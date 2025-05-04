module.exports = {
  apps: [{
    name: "2anki-backend",
    script: "./backend/main.py",
    interpreter: "python3",
    args: "--reload",
    env: {
      NODE_ENV: "development",
      PORT: 8000,
    },
    env_production: {
      NODE_ENV: "production",
      PORT: 8000,
    },
  }],
};
