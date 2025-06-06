module.exports = {
  apps: [
    {
      name: "tuneAPI-1",
      script: "./venv/bin/uvicorn",
      interpreter: "./venv/bin/python",
      args: "main:app --host 0.0.0.0 --port 8000",
      cwd: "/home/admin77/Backend/backend",
      watch: false,
      env: {
        PYTHONUNBUFFERED: "1",
      },
    },
  ],
};
