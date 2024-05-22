import streamlit as st
import requests

# Pushover API adatok (éles kulcsok)
PUSHOVER_API_TOKEN = "anw4j6o8ycyg2jou2iapr2u79avydq"
PUSHOVER_USER_KEY = "urmeuez42s27uma7rqvx5av92hj2ad"

# Alkalmazás címének beállítása
st.title("Anna 10. szülinapi visszajelzés")

# Űrlap állapotának nyomon követése (Session State használata)
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

if not st.session_state.form_submitted:  # Csak akkor jelenjen meg az űrlap, ha még nem küldték el
    # Űrlap létrehozása
    with st.form(key='event_form'):
        name = st.text_input("Név:")
        attendance = st.radio("Tudsz jönni Anna szülinapi bulijára?", ("Igen", "Nem"), index=None)
        submit_button = st.form_submit_button(label='Elküld')

    # Űrlap elküldésekor
    if submit_button:
        st.session_state.form_submitted = True  # Űrlap elküldve jelzése
        st.info("Mentés folyamatban...")  # Visszajelzés a felhasználónak

        # Pushover értesítés küldése (mindkét esetben)
        if attendance == "Igen":
            message = f"{name} részt vesz Anna szülinapi buliján!"
        else:
            message = f"{name} nem tud részt venni Anna szülinapi buliján."

        data = {
            "token": PUSHOVER_API_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "message": message
        }
        response = requests.post("https://api.pushover.net/1/messages.json", data=data)

        # Visszajelzés a felhasználónak a PUSHOVER válasza után
        if response.status_code == 200:
            st.success("Visszajelzés elküldve, köszönjük!")
        else:
            st.error(f"Hiba történt az értesítés küldése során. Hibakód: {response.status_code}")

# Ha az űrlap már el lett küldve, csak a visszajelzés jelenik meg
elif st.session_state.form_submitted:
    st.info("Mentés folyamatban...") # Ezt a sort törölheted, ha nem akarod, hogy megjelenjen

