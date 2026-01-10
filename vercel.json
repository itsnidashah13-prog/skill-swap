{
  "version": 2,
  "name": "skill-swap",
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.9"
  },
  "functions": {
    "main.py": {
      "runtime": "python3.9"
    }
  }
}
