"""
Helper script to set up voice dependencies and test voice functionality
"""
import subprocess
import sys
import platform

def install_voice_dependencies():
    """Install voice-related dependencies"""
    print("Installing voice dependencies...")
    
    # Base packages
    packages = ["SpeechRecognition", "pyttsx3"]
    
    # Platform-specific packages
    if platform.system() == "Windows":
        packages.append("pyaudio")
    elif platform.system() == "Darwin":  # macOS
        print("For macOS, you may need to install PortAudio first:")
        print("brew install portaudio")
        packages.append("pyaudio")
    else:  # Linux
        print("For Linux, you may need to install dependencies first:")
        print("sudo apt-get install python3-pyaudio portaudio19-dev")
        packages.append("pyaudio")
    
    # Install packages
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")
            print(f"Try manually: pip install {package}")

def test_voice():
    """Test voice functionality"""
    print("\nTesting voice functionality...")
    
    try:
        # Test speech recognition
        import speech_recognition as sr
        r = sr.Recognizer()
        print("✅ Speech recognition imported successfully")
        
        # Test microphone
        try:
            mic = sr.Microphone()
            print("Microphone detected")
        except Exception as e:
            print(f" Microphone error: {e}")
        
        # Test text-to-speech
        import pyttsx3
        engine = pyttsx3.init()
        print("Text-to-speech initialized")
        
        # Test speaking
        engine.say("Voice system is working")
        engine.runAndWait()
        print("Text-to-speech test complete")
        
        print("\n✨ Voice setup complete! You can now use voice features.")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please install missing dependencies")
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    print("Voice Setup Assistant")
    print("=" * 50)
    
    response = input("Install voice dependencies? (y/n): ")
    if response.lower() == 'y':
        install_voice_dependencies()
    
    print("\n" + "=" * 50)
    test_voice()