# RSA Secure Messenger Demo

An interactive educational tool demonstrating the RSA public-key cryptosystem using Streamlit.

## 📖 Overview

RSA (Rivest–Shamir–Adleman) is one of the foundational public-key cryptosystems. This application provides a step-by-step interactive demonstration of how RSA encryption works, from key generation to encryption/decryption, along with attack demonstrations and quantum threats.

### Key Features

- **Interactive Key Generation**: Generate RSA key pairs with customizable bit sizes
- **Step-by-Step Encryption**: Encrypt messages character-by-character with visual feedback
- **Decryption Process**: Decrypt messages and verify integrity with hashing
- **Attack Demonstration**: Explore the factorization problem that underlies RSA security
- **Quantum Threats**: Learn about Shor's algorithm and quantum computing threats to RSA
- **Educational Focus**: Clean, intuitive interface designed for learning cryptography

## 🚀 Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Setup

1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   cd rsa-demo
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📋 Requirements

- streamlit
- pandas

## 🎯 Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser to the provided URL (usually http://localhost:8501)

3. Navigate through the steps:
   - **Home**: Introduction and overview
   - **Key Generation**: Create RSA key pairs
   - **Encryption**: Encrypt messages using public keys
   - **Decryption**: Decrypt messages using private keys
   - **Attack Demo**: Try factoring small numbers
   - **About RSA**: Learn more about the algorithm
   - **Quantum Threats**: Understand quantum computing risks

## 🔧 Project Structure

```
rsa-demo/
├── app.py              # Main Streamlit application
├── rsa_lib.py          # RSA implementation library
├── test_rsa.py         # Unit tests for RSA functions
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🧪 Testing

Run the test suite to verify RSA implementation:

```bash
python test_rsa.py
```

## 🔐 Security Notes

- This is an educational tool only
- Uses small key sizes for demonstration (not secure for real use)
- Real RSA implementations use much larger keys (2048+ bits)
- Quantum computers pose a future threat via Shor's algorithm

## 📚 Learn More

- [RSA on Wikipedia](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
- [Khan Academy Cryptography](https://www.khanacademy.org/computing/computer-science/cryptography)
- [Shor's Algorithm](https://en.wikipedia.org/wiki/Shor%27s_algorithm)

## 🤝 Contributing

This is an educational project. Feel free to suggest improvements or report issues.

## 📄 License

Educational use only. See individual components for licensing details.