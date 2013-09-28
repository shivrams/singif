from app import frontend_app, backend_app
from config import SINGIF_IS_LIVE

if __name__ == "__main__":
    if SINGIF_IS_LIVE:
        frontend_app.run()
        backend_app.run()
    else:
        frontend_app.run(debug=True)
        backend_app.run(debug=True)
