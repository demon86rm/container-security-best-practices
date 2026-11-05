package main

import (
	"context"
	"encoding/json"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func envOrDefault(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func main() {
	// 12-Factor XI: logs are an event stream on stdout, one JSON object per line.
	log := slog.New(slog.NewJSONHandler(os.Stdout, nil))

	// 12-Factor III and VII: config comes from the environment, not from the image.
	port := envOrDefault("PORT", "8080")
	appEnv := envOrDefault("APP_ENV", "local")

	mux := http.NewServeMux()

	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{
			"app": "demo-app",
			"env": appEnv,
		})
	})

	// The platform probes, not the developer.
	mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("ok"))
	})
	mux.HandleFunc("/readyz", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("ok"))
	})

	srv := &http.Server{
		Addr:              ":" + port,
		Handler:           mux,
		ReadHeaderTimeout: 5 * time.Second, // no Slowloris: a security workshop app must not leak connections
	}

	// 12-Factor IX: disposability. On SIGTERM stop accepting, finish in-flight requests, exit.
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGTERM, syscall.SIGINT)
	defer stop()
	go func() {
		<-ctx.Done()
		log.Info("shutting down")
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		srv.Shutdown(shutdownCtx)
	}()

	log.Info("demo-app starting", "env", appEnv, "port", port)
	if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Error("server error", "err", err)
		os.Exit(1)
	}
}
