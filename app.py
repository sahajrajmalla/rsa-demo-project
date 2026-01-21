import streamlit as st
import time
import pandas as pd
import rsa_lib

# Page Config
st.set_page_config(
    page_title="RSA Secure Messenger",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for minimalist design
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #34495e;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #bdc3c7;
        padding-bottom: 0.5rem;
    }
    .card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ecf0f1;
        margin-bottom: 1rem;
    }
    .math-box {
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        margin: 0.5rem 0;
        border-left: 3px solid #3498db;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 4px;
        border: 1px solid #c3e6cb;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.5rem;
        border-radius: 4px;
        border: 1px solid #f5c6cb;
    }
    .stButton>button {
        border-radius: 4px;
        height: 2.5em;
        font-weight: 500;
    }
    .highlight {
        background-color: #ecf0f1;
        padding: 0.5rem;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'key_generated' not in st.session_state:
    st.session_state.key_generated = False
if 'public_key' not in st.session_state:
    st.session_state.public_key = None
if 'private_key' not in st.session_state:
    st.session_state.private_key = None
if 'p' not in st.session_state: st.session_state.p = None
if 'q' not in st.session_state: st.session_state.q = None
if 'n' not in st.session_state: st.session_state.n = None
if 'phi' not in st.session_state: st.session_state.phi = None
if 'e' not in st.session_state: st.session_state.e = None
if 'd' not in st.session_state: st.session_state.d = None
if 'encrypted_message' not in st.session_state:
    st.session_state.encrypted_message = None
if 'original_message_hash' not in st.session_state:
    st.session_state.original_message_hash = None
if 'decrypted_message' not in st.session_state:
    st.session_state.decrypted_message = None

# Sidebar Navigation
st.sidebar.title("🔐 RSA Demo")
page = st.sidebar.radio("Navigate", [
    "Home",
    "1. Key Generation (Bob)",
    "2. Encryption (Alice)",
    "3. Decryption (Bob)",
    "4. Attack Demo",
    "5. About RSA",
    "6. Quantum Threats"
])

st.sidebar.markdown("---")
st.sidebar.info("This is an educational tool to demonstrate how RSA encryption works step-by-step.")

# --- HOME PAGE ---
if page == "Home":
    st.markdown('<div class="main-header">RSA Public-Key Cryptosystem</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### Welcome!
        RSA (Rivest–Shamir–Adleman) is one of the first public-key cryptosystems and is widely used for secure data transmission.
        
        In this cryptosystem, the encryption key is public and it is different from the decryption key which is kept secret (private).
        
        **How to use this demo:**
        1.  **Generate Keys**: Bob creates a Public Key (to share) and a Private Key (to keep).
        2.  **Encrypt**: Alice uses Bob's Public Key to lock a message.
        3.  **Decrypt**: Bob uses his Private Key to unlock the message.
        """)
    
    with col2:
        st.markdown("""
        ### Communication Flow
        ```
        Alice                    Bob
          |                       |
          |  Public Key (e,n)     |
          | <--------------------- |
          |                       |
          |  Encrypted Message    |
          | ------------------->  |
          |                       |
          |  Private Key (d,n)    |
          |      (secret)         |
        ```
        """)

# --- KEY GENERATION PAGE ---
elif page == "1. Key Generation (Bob)":
    st.markdown('<div class="main-header">Step 1: Key Generation</div>', unsafe_allow_html=True)
    st.markdown("Bob needs to generate a pair of keys: one public (for Alice) and one private (for himself).")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            key_size = st.select_slider(
                "Select Key Size (bits)",
                options=[8, 16, 32, 64, 128, 256, 512, 1024],
                value=64,
                help="Larger keys are more secure but slower. For this demo, small keys (8-64 bits) are good for visualization."
            )
        with col2:
            st.write("") # Spacer
            st.write("") # Spacer
            generate_btn = st.button("Generate Key Pair", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    if generate_btn:
        with st.spinner("Generating primes and calculating keys..."):
            # Artificial delay for effect
            time.sleep(0.5)
            
            # 1. Generate p and q
            ((e, n), (d, n), p, q, phi) = rsa_lib.generate_keypair(key_size)
            
            # Store in session state
            st.session_state.key_generated = True
            st.session_state.public_key = (e, n)
            st.session_state.private_key = (d, n)
            st.session_state.p = p
            st.session_state.q = q
            st.session_state.n = n
            st.session_state.phi = phi
            st.session_state.e = e
            st.session_state.d = d
            
            st.success("Keys Generated Successfully!")

    if st.session_state.key_generated:
        st.markdown("### 🔍 Key Generation Steps")
        
        with st.expander("Step 1: Generate Two Primes", expanded=True):
            st.markdown('<div class="math-box">', unsafe_allow_html=True)
            st.latex(f"p = {st.session_state.p} \\quad q = {st.session_state.q}")
            st.markdown("Two large random prime numbers.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander("Step 2: Compute Modulus"):
            st.markdown('<div class="math-box">', unsafe_allow_html=True)
            st.latex(f"n = p \\times q = {st.session_state.p} \\times {st.session_state.q} = {st.session_state.n}")
            st.markdown("The modulus used in both keys.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander("Step 3: Euler's Totient"):
            st.markdown('<div class="math-box">', unsafe_allow_html=True)
            st.latex(f"\\phi(n) = (p-1) \\times (q-1) = ({st.session_state.p}-1) \\times ({st.session_state.q}-1) = {st.session_state.phi}")
            st.markdown("Number of integers up to n that are coprime with n.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander("Step 4: Choose Public Exponent"):
            st.markdown('<div class="math-box">', unsafe_allow_html=True)
            st.latex(f"e = {st.session_state.e}")
            st.markdown("Chosen such that gcd(e, φ(n)) = 1.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander("Step 5: Compute Private Exponent"):
            st.markdown('<div class="math-box">', unsafe_allow_html=True)
            st.latex(f"d \\equiv e^{{-1}} \\pmod{{\\phi(n)}} = {st.session_state.d}")
            st.markdown("The modular inverse of e modulo φ(n).")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 🔑 Your Keys")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="highlight">', unsafe_allow_html=True)
            st.markdown("**Public Key** (share this)")
            st.code(f"(e={st.session_state.e}, n={st.session_state.n})")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="highlight">', unsafe_allow_html=True)
            st.markdown("**Private Key** (keep secret)")
            st.code(f"(d={st.session_state.d}, n={st.session_state.n})")
            st.markdown('</div>', unsafe_allow_html=True)

# --- ENCRYPTION PAGE ---
elif page == "2. Encryption (Alice)":
    st.markdown('<div class="main-header">Step 2: Encryption</div>', unsafe_allow_html=True)
    
    if not st.session_state.key_generated:
        st.warning("⚠️ Bob hasn't generated keys yet! Go to Step 1.")
    else:
        st.markdown("Alice wants to send a secret message to Bob. She uses Bob's **Public Key**.")
        
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            message = st.text_input("Enter your message:", "Hello RSA!")
            
            if st.button("Encrypt Message", type="primary"):
                if not message:
                    st.error("Please enter a message.")
                else:
                    # Encrypt
                    st.session_state.encrypted_message = rsa_lib.encrypt_message(st.session_state.public_key, message)
                    st.session_state.original_message_hash = rsa_lib.compute_hash(message)
                    
                    st.success("Message Encrypted!")
                    
                    st.markdown("### 🔢 Encryption Process")
                    st.markdown("Each character is encrypted as: $c = m^e \\mod n$")
                    
                    # Show first few characters
                    for i, (char, cipher) in enumerate(zip(message[:5], st.session_state.encrypted_message[:5])):
                        col1, col2, col3 = st.columns([1,2,2])
                        with col1:
                            st.markdown(f"**'{char}'**")
                        with col2:
                            st.markdown(f"ASCII: {ord(char)}")
                        with col3:
                            st.markdown(f"Cipher: {cipher}")
                    
                    if len(message) > 5:
                        st.markdown(f"... and {len(message)-5} more characters")
                    
                    st.markdown("### 📦 The Ciphertext")
                    st.code(str(st.session_state.encrypted_message), language="python")
                    st.caption("This encrypted data is sent to Bob.")
            st.markdown('</div>', unsafe_allow_html=True)

# --- DECRYPTION PAGE ---
elif page == "3. Decryption (Bob)":
    st.markdown('<div class="main-header">Step 3: Decryption</div>', unsafe_allow_html=True)
    
    if not st.session_state.encrypted_message:
        st.warning("⚠️ No message has been encrypted yet! Go to Step 2.")
    else:
        st.markdown("Bob receives the ciphertext and uses his **Private Key** to read it.")
        
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Received Ciphertext")
            st.code(str(st.session_state.encrypted_message), language="json")
            
            if st.button("Decrypt Message", type="primary"):
                # Decrypt
                decrypted = rsa_lib.decrypt_message(st.session_state.private_key, st.session_state.encrypted_message)
                st.session_state.decrypted_message = decrypted
                
                st.markdown("### 🔓 Decryption Process")
                st.markdown("Each ciphertext number is decrypted as: $m = c^d \\mod n$")
                
                # Show first few
                for i, (cipher, char) in enumerate(zip(st.session_state.encrypted_message[:5], decrypted[:5])):
                    col1, col2, col3 = st.columns([2,1,1])
                    with col1:
                        st.markdown(f"Cipher: {cipher}")
                    with col2:
                        st.markdown(f"ASCII: {ord(char)}")
                    with col3:
                        st.markdown(f"**'{char}'**")
                
                if len(decrypted) > 5:
                    st.markdown(f"... and {len(decrypted)-5} more characters")
                
                st.markdown("### 📜 The Result")
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown(f"**Decrypted Message:** {decrypted}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Integrity Check
                current_hash = rsa_lib.compute_hash(decrypted)
                st.markdown("#### 🛡️ Integrity Check")
                if current_hash == st.session_state.original_message_hash:
                    st.success(f"✅ Hash matches: {current_hash[:16]}...")
                else:
                    st.error("❌ Hash mismatch!")
            st.markdown('</div>', unsafe_allow_html=True)

# --- ATTACK DEMO PAGE ---
elif page == "4. Attack Demo":
    st.markdown('<div class="main-header">💥 Attack Demonstration</div>', unsafe_allow_html=True)
    st.markdown("Why is RSA secure? Because factoring large numbers is **hard**.")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### The Factorization Problem")
    st.markdown("The public key contains $n = p \\times q$. If an attacker can factor $n$ into $p$ and $q$, they can calculate $\phi(n)$ and then the private key $d$.")
    
    st.markdown("#### Try it yourself!")
    st.markdown("Here is a small $n$. Can you find $p$ and $q$?")
    
    challenge_p = 61
    challenge_q = 53
    challenge_n = challenge_p * challenge_q
    
    st.latex(f"n = {challenge_n}")
    
    col1, col2 = st.columns(2)
    with col1:
        guess_p = st.number_input("Guess p:", min_value=2, step=1)
    with col2:
        guess_q = st.number_input("Guess q:", min_value=2, step=1)
        
    if st.button("Check Factors"):
        if guess_p * guess_q == challenge_n and guess_p > 1 and guess_q > 1:
            st.success(f"Correct! {guess_p} * {guess_q} = {challenge_n}")
            st.balloons()
        else:
            st.error(f"Incorrect. {guess_p} * {guess_q} = {guess_p * guess_q} (Target: {challenge_n})")
            
    st.markdown("---")
    st.markdown("### Real World Security")
    st.markdown("""
    In the real world, $n$ is 2048 bits (about 617 digits).
    
    - **Small n (15 bits)**: Instant to factor.
    - **Medium n (256 bits)**: Minutes/Hours on a PC.
    - **Large n (2048 bits)**: Billions of years on a supercomputer.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ABOUT PAGE ---
elif page == "5. About RSA":
    st.markdown('<div class="main-header">About RSA</div>', unsafe_allow_html=True)
    st.markdown("""
    **RSA (Rivest–Shamir–Adleman)** is a public-key cryptosystem that is widely used for secure data transmission. It is also one of the oldest.
    
    The acronym RSA comes from the surnames of Ron Rivest, Adi Shamir, and Leonard Adleman, who publicly described the algorithm in 1977.
    
    ### Key Concepts
    1.  **Asymmetric Encryption**: Uses two different keys (public and private).
    2.  **Trapdoor Function**: Easy to compute in one direction, hard to reverse without special information (the private key).
    3.  **Prime Factorization**: The security relies on the practical difficulty of factoring the product of two large prime numbers.
    
    ### References
    - [Wikipedia: RSA (cryptosystem)](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
    - [Khan Academy: Journey into Cryptography](https://www.khanacademy.org/computing/computer-science/cryptography)
    """)

# --- QUANTUM THREATS PAGE ---
elif page == "6. Quantum Threats":
    st.markdown('<div class="main-header">⚛️ Quantum Threats to RSA</div>', unsafe_allow_html=True)
    st.markdown("RSA's security relies on the difficulty of factoring large numbers. Quantum computers threaten this with **Shor's Algorithm**.")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Why Quantum Computers Break RSA")
    st.markdown("""
    Classical computers factor numbers using trial division or advanced methods, but it's exponential time.
    
    Quantum computers use **Shor's Algorithm** (1994) to factor in polynomial time using quantum Fourier transform.
    
    This breaks RSA because once p and q are found, φ(n) and d can be computed easily.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Shor's Algorithm Overview")
    st.markdown("""
    1. **Quantum Period Finding**: Find the period of f(x) = a^x mod N
    2. **Classical Post-Processing**: Use the period to find factors
    3. **Repeat**: Until factors are found
    """)
    st.latex(r"f(x) = a^x \mod N")
    st.markdown("If r is the period, and r is even, then gcd(a^{r/2} ± 1, N) may give factors.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Practical Demo: Factoring Small N")
    st.markdown("Try factoring a small n classically (what quantum does instantly for large n).")
    
    demo_n = st.number_input("Enter a small composite number N (e.g., 15, 21, 35):", min_value=4, value=15, step=1)
    
    if st.button("Factor N"):
        factors = []
        for i in range(2, int(demo_n**0.5) + 1):
            if demo_n % i == 0:
                factors = [i, demo_n // i]
                break
        if factors:
            st.success(f"Factors: {factors[0]} × {factors[1]} = {demo_n}")
            st.markdown("Quantum computers can do this for 2048-bit n in seconds!")
        else:
            st.error("N is prime or too large for demo.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Real-World Impact")
    st.markdown("""
    - **Current Status**: No quantum computer can break 2048-bit RSA yet.
    - **Transition**: Cryptographers recommend moving to post-quantum algorithms like lattice-based crypto.
    - **Timeline**: Experts predict quantum advantage by 2030-2040.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
