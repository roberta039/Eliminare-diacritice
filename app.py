import streamlit as st

# Configurare pagină
st.set_page_config(
    page_title="Eliminare Diacritice",
    page_icon="🇷🇴",
    layout="centered"
)

# CSS custom
st.markdown("""
<style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .title {
        text-align: center;
        color: #1E3A5F;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    /* Stil pentru textarea */
    textarea {
        font-size: 16px !important;
    }
    /* Stil pentru rezultat */
    .result-box {
        background-color: #f0f2f6;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 20px;
        font-size: 16px;
        line-height: 1.6;
        margin: 10px 0;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .copy-info {
        text-align: center;
        color: #888;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Mapping diacritice românești -> caractere fără diacritice
DIACRITICE_MAP = {
    'ă': 'a', 'Ă': 'A',
    'â': 'a', 'Â': 'A',
    'î': 'i', 'Î': 'I',
    'ș': 's', 'Ș': 'S',
    'ț': 't', 'Ț': 'T',
    # Variante cu sedilă (vechi, din unele fonturi)
    'ş': 's', 'Ş': 'S',
    'ţ': 't', 'Ţ': 'T',
}

def elimina_diacritice(text: str) -> str:
    """Elimină diacriticele românești din text."""
    rezultat = []
    for char in text:
        rezultat.append(DIACRITICE_MAP.get(char, char))
    return ''.join(rezultat)


# --- UI ---
st.markdown('<h1 class="title">🇷🇴 Eliminare Diacritice</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transformă textul românesc cu diacritice în text fără diacritice</p>', unsafe_allow_html=True)

# Input
text_input = st.text_area(
    "📝 Introdu textul cu diacritice:",
    height=200,
    placeholder="Scrie sau lipește aici textul cu diacritice...\n\nExemplu: Româniaește o țară frumoasă, cu câmpii și munți înalți."
)

# Butoane pe un rând
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    convert_btn = st.button("🔄 Transformă", use_container_width=True, type="primary")

# Procesare și afișare rezultat
if text_input:
    text_output = elimina_diacritice(text_input)

    st.markdown("---")
    st.markdown("### ✅ Text fără diacritice:")

    # Afișăm rezultatul
    st.markdown(f'<div class="result-box">{text_output}</div>', unsafe_allow_html=True)

    # Buton COPY folosind JavaScript nativ prin st.components
    # Streamlit nu are copy nativ, folosim un workaround cu st.code sau JS
    
    # Metodă 1: text_area readonly (ușor de selectat și copiat)
    st.text_area(
        "Selectează tot textul de mai jos și copiază (Ctrl+A, Ctrl+C):",
        value=text_output,
        height=200,
        key="output_area"
    )

    # Metodă 2: Buton Copy cu JavaScript
    st.markdown(f"""
    <button onclick="copyToClipboard()" style="
        background-color: #4CAF50;
        color: white;
        padding: 12px 30px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        display: block;
        margin: 10px auto;
        transition: background-color 0.3s;
    " onmouseover="this.style.backgroundColor='#45a049'" 
      onmouseout="this.style.backgroundColor='#4CAF50'">
        📋 Copiază Textul
    </button>
    <p id="copy-status" class="copy-info"></p>
    
    <textarea id="hidden-text" style="position:absolute;left:-9999px;">{text_output}</textarea>
    
    <script>
    function copyToClipboard() {{
        const text = document.getElementById('hidden-text').value;
        navigator.clipboard.writeText(text).then(function() {{
            document.getElementById('copy-status').innerHTML = '✅ Text copiat cu succes!';
            setTimeout(function() {{
                document.getElementById('copy-status').innerHTML = '';
            }}, 3000);
        }}, function() {{
            // Fallback
            const el = document.getElementById('hidden-text');
            el.style.position = 'fixed';
            el.style.left = '0';
            el.select();
            document.execCommand('copy');
            el.style.position = 'absolute';
            el.style.left = '-9999px';
            document.getElementById('copy-status').innerHTML = '✅ Text copiat cu succes!';
            setTimeout(function() {{
                document.getElementById('copy-status').innerHTML = '';
            }}, 3000);
        }});
    }}
    </script>
    """, unsafe_allow_html=True)

    # Statistici
    st.markdown("---")
    nr_diacritice = sum(1 for c in text_input if c in DIACRITICE_MAP)
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("📊 Caractere totale", len(text_input))
    col_s2.metric("🔤 Diacritice găsite", nr_diacritice)
    col_s3.metric("📝 Cuvinte", len(text_input.split()))

else:
    # Exemplu demonstrativ
    st.markdown("---")
    st.info("👆 Introdu un text mai sus pentru a elimina diacriticele.")
    
    st.markdown("#### Exemple de transformări:")
    exemple = {
        "România": "Romania",
        "țară": "tara",
        "câmpii": "campii",
        "munți": "munti",
        "înalți": "inalti",
        "fârșit": "farsit",
        "această": "aceasta",
    }
    
    for cu, fara in exemple.items():
        st.markdown(f"- **{cu}** → **{fara}**")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align:center; color:#999; font-size:13px;">'
    'Creat cu ❤️ folosind Streamlit | '
    'Funcționează cu ă, â, î, ș, ț (și variantele cu sedilă)'
    '</p>',
    unsafe_allow_html=True
)
