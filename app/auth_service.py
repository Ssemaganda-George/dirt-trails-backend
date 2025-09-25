import requests
import jwt  # PyJWT

# --- Google token verification ---
def verify_google_token(id_token: str):
    """
    Verify Google ID token using Google's tokeninfo endpoint.
    """
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    data = resp.json()
    return {
        "email": data["email"],
        "name": data.get("name"),
        "google_id": data["sub"]
    }

# --- Apple token verification ---
def verify_apple_token(identity_token: str):
    """
    Decode Apple identity token without verifying signature (demo only).
    For production, you must verify using Apple's public keys.
    """
    try:
        # Decode token without signature verification
        decoded = jwt.decode(identity_token, options={"verify_signature": False})
        return {
            "email": decoded.get("email"),
            "name": decoded.get("name"),
            "apple_id": decoded.get("sub")
        }
    except jwt.PyJWTError:
        return None
