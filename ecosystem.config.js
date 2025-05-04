module.exports = {
  apps: [{
    name: "napi",
    script: "./backend/main.py",
    interpreter: "python3",
    args: "--reload",
    env: {
      NODE_ENV: "development",
      PORT: 31415,
    },
    env_production: {
      NODE_ENV: "production",
      PORT: 31415,
    },
  }],
};
