import streamlit as st


def loader():
    st.markdown(
        """
        <style>
        .loading-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 80vh;
            gap: 40px;
        }

        /* Calima Blob Animation */
        .loading-blob {
            width: 80px;
            height: 80px;
            background: linear-gradient(45deg, #FF8C42, #F9C784, #E07A5F);
            background-size: 200% 200%;
            border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
            animation:
                blob-morph 4s ease-in-out infinite,
                blob-color 6s ease infinite,
                blob-rotate 10s linear infinite;
            filter: blur(2px);
            box-shadow: 0 0 20px rgba(255, 140, 66, 0.3);
        }

        @keyframes blob-morph {
            0%, 100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
            50% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }
        }

        @keyframes blob-color {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes blob-rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .loading-text {
            font-size: 1.2rem;
            font-family: 'PlusJakarta', sans-serif;
            text-align: center;
            line-height: 1.5;
            letter-spacing: -0.01em;
            opacity: 0.9;
        }

        .loading-text b {
            color: #E07A5F;
            font-family: 'Zodiak', serif;
        }
        </style>

        <div class="loading-container">
            <div class="loading-blob"></div>
            <div class="loading-text">
                ¡Hola!<br>
                estamos abriendo <b>Kalima</b>...
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )
