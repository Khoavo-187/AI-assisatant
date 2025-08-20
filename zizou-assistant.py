from gtts import gTTS
import pygame
from google import genai
from google.genai import types
import speech_recognition
import streamlit as st
import tempfile
import os
from PIL import Image
import base64
import io
import threading
import time
import wave

# Enhanced page configuration
st.set_page_config(
    page_title="Zizou AI Assistant", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
/* Import modern fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Main app styling */
.main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* Custom background overlay */
.stApp {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    color: white;
}

/* Sidebar styling */
.css-1d391kg {
    background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    border-right: 2px solid #3498db;
}

/* Title styling */
h1 {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    color: #ffffff;
    text-align: center;
    font-size: 3rem;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    background: linear-gradient(45deg, #3498db, #e74c3c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle styling */
h3 {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    color: #ecf0f1;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

/* Card-like containers */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #ecf0f1;
    border-radius: 10px;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(45deg, #3498db, #2ecc71);
    color: white;
}

/* Button styling */
.stButton button {
    background: linear-gradient(45deg, #3498db, #2ecc71);
    color: white;
    border: none;
    border-radius: 12px;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    padding: 12px 24px;
    box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
    transition: all 0.3s ease;
}

.stButton button:hover {
    background: linear-gradient(45deg, #2980b9, #27ae60);
    box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
    transform: translateY(-2px);
}

/* Input fields styling */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 10px;
    color: white;
    backdrop-filter: blur(5px);
    font-family: 'Inter', sans-serif;
}

.stTextArea textarea::placeholder, .stTextInput input::placeholder {
    color: rgba(255,255,255,0.7);
}

/* Success/Error messages */
.stSuccess {
    background: linear-gradient(45deg, #2ecc71, #27ae60);
    border-radius: 10px;
    border: none;
    color: white;
}

.stError {
    background: linear-gradient(45deg, #e74c3c, #c0392b);
    border-radius: 10px;
    border: none;
    color: white;
}

.stInfo {
    background: linear-gradient(45deg, #3498db, #2980b9);
    border-radius: 10px;
    border: none;
    color: white;
}

.stWarning {
    background: linear-gradient(45deg, #f39c12, #e67e22);
    border-radius: 10px;
    border: none;
    color: white;
}

/* File uploader styling */
.stFileUploader {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    border: 2px dashed rgba(255,255,255,0.3);
    backdrop-filter: blur(10px);
}

/* Columns styling */
.stColumn {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    margin: 10px 5px;
}

/* Spinner styling */
.stSpinner {
    color: #3498db;
}

/* Code block styling */
.stCode {
    background: rgba(0,0,0,0.3);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.2);
}

/* Metric styling */
.metric-container {
    background: linear-gradient(135deg, rgba(52, 152, 219, 0.2), rgba(46, 204, 113, 0.2));
    border-radius: 15px;
    padding: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    text-align: center;
    margin: 10px 0;
}

/* Chat bubble styling */
.user-message {
    background: linear-gradient(45deg, #3498db, #2980b9);
    border-radius: 20px 20px 5px 20px;
    padding: 15px;
    margin: 10px 0;
    color: white;
    max-width: 80%;
    margin-left: auto;
    box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
}

.assistant-message {
    background: linear-gradient(45deg, #2ecc71, #27ae60);
    border-radius: 20px 20px 20px 5px;
    padding: 15px;
    margin: 10px 0;
    color: white;
    max-width: 80%;
    box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3);
}

/* Professional status indicators */
.status-online {
    display: inline-block;
    width: 12px;
    height: 12px;
    background: #2ecc71;
    border-radius: 50%;
    animation: pulse 2s infinite;
    margin-right: 8px;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(46, 204, 113, 0); }
    100% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); }
}

/* Voice wave animation */
.voice-wave {
    display: inline-block;
    margin-right: 8px;
}

.voice-wave span {
    display: inline-block;
    width: 4px;
    height: 20px;
    background: #3498db;
    margin: 0 2px;
    animation: wave 1s ease-in-out infinite;
}

.voice-wave span:nth-child(2) { animation-delay: 0.1s; }
.voice-wave span:nth-child(3) { animation-delay: 0.2s; }
.voice-wave span:nth-child(4) { animation-delay: 0.3s; }

@keyframes wave {
    0%, 100% { height: 20px; }
    50% { height: 5px; }
}

/* Sidebar enhancements */
.sidebar-header {
    background: linear-gradient(45deg, #3498db, #2ecc71);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

client = genai.client(
    api_key="AIzaSyDCug_95N5QwzPhF_HqTU7S8KYgJQhDO0Y"
)

# Initialize pygame mixer properly
pygame.mixer.pre_init(frequency=44200, size=-16, channels=2, buffer=1024)
pygame.mixer.init()

robot_ear = speech_recognition.Recognizer()
robot_brain = "" 

# Enhanced Zizou personality configurations
PERSONALITY_CONFIGS = {
    "professional": {
        "name": "Chuyên nghiệp",
        "prompt": """
        Tôi với tư cách là chủ của doanh nghiệp quản lí cát toàn quốc (gọi tôi là lượm)
        Bạn là một trợ lí chuyên nghiệp của tôi, thông minh và nhanh nhẹn.
        Hãy trả lời một cách:
        - Chuyên nghiệp và chính xác
        - Biết cách diễn đạt
        - Tự tin và nhanh chóng
        - Luôn sẵn sàng giúp đỡ
        - Khả năng xoay sở tình huống tuyệt vời, tư duy hơn người
        
        Khi được cung cấp hình ảnh hoặc file, hãy phân tích chi tiết và giải thích một cách dễ hiểu.
        Hãy báo cáo như 1 trợ lí chuyên nghiệp trong lĩnh vực kinh tế
        Trả lời bằng tiếng Việt.
        """
    },
    "friendly": {
        "name": "Thân thiện",
        "prompt": """
        Bạn là Zizou, một AI assistant thân thiện và gần gũi.
        Hãy trả lời với phong cách:
        - Ấm áp và gần gũi
        - Nhiệt tình giúp đỡ
        - Dễ hiểu và đơn giản
        - Có thể sử dụng emoji phù hợp
        - Giọng điệu thoải mái, không quá nghiêm túc
        
        Luôn sẵn sàng giải thích và hỗ trợ người dùng.
        Trả lời bằng tiếng Việt.
        """
    },
    "academic": {
        "name": "Học thuật",
        "prompt": """
        Bạn là một chuyên gia học thuật với kiến thức sâu rộng.
        Phong cách trả lời:
        - Chi tiết và có căn cứ
        - Sử dụng thuật ngữ chuyên môn khi cần
        - Phân tích sâu sắc
        - Đưa ra nhiều góc nhìn khác nhau
        - Trích dẫn thông tin đáng tin cậy
        
        Luôn cố gắng giáo dục và cung cấp thông tin có giá trị.
        Trả lời bằng tiếng Việt.
        """
    },
    "creative": {
        "name": "Sáng tạo",
        "prompt": """
        Bạn là một AI assistant sáng tạo và đầy cảm hứng.
        Phong cách trả lời:
        - Sáng tạo và độc đáo
        - Sử dụng ẩn dụ và hình ảnh sinh động
        - Khuyến khích tư duy mới
        - Đưa ra nhiều ý tưởng khác nhau
        - Có thể sử dụng câu chuyện minh họa
        
        Luôn cố gắng truyền cảm hứng và động lực.
        Trả lời bằng tiếng Việt.
        """
    }
}

# Enhanced voice options
VOICE_OPTIONS = {
    "Kore (Gemini TTS)": {
        "model": "gemini-2.5-flash-preview-tts",
        "voice": "Kore",
        "description": "Giọng nói AI chất lượng cao, tự nhiên"
    },
    "Aoede (Gemini TTS)": {
        "model": "gemini-2.5-flash-preview-tts", 
        "voice": "Aoede",
        "description": "Giọng nói nữ mượt mà, dễ nghe"
    },
    "Charon (Gemini TTS)": {
        "model": "gemini-2.5-flash-preview-tts",
        "voice": "Charon", 
        "description": "Giọng nói nam trầm ấm"
    },
    "Fenrir (Gemini TTS)": {
        "model": "gemini-2.5-flash-preview-tts",
        "voice": "Fenrir",
        "description": "Giọng nói năng động, mạnh mẽ"
    },
    "Vietnamese (gTTS)": {
        "model": "gtts",
        "voice": "vi",
        "description": "Giọng tiếng Việt truyền thống"
    }
}

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Helper function to save wave file"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

def speak_with_gemini_voice(text, voice_name="Kore"):
    """Enhanced TTS using Gemini's voice options"""
    try:
        # Clean text for speech
        clean_text = text.replace("*", "").replace("#", "").strip()
        if not clean_text:
            return False
            
        # Generate speech using Gemini with selected voice
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=clean_text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name,
                        )
                    )
                ),
            )
        )
        
        # Extract audio data
        audio_data = response.candidates[0].content.parts[0].inline_data.data
        
        # Use temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            wave_file(tmp_file.name, audio_data)
            temp_path = tmp_file.name
        
        # Play with pygame
        pygame.mixer.quit()
        pygame.mixer.pre_init(frequency=44200, size=-16, channels=1, buffer=1024)
        pygame.mixer.init()
        
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play()
        
        # Wait for playback to complete
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        
        # Cleanup
        pygame.mixer.music.stop()
        os.unlink(temp_path)
        
        return True
        
    except Exception as e:
        st.error(f"🔊 Lỗi phát âm thanh với {voice_name} voice: {e}")
        # Fallback to gTTS if voice fails
        return speak_with_gtts_fallback(text)

def speak_with_gtts_fallback(text):
    """Fallback TTS using gTTS"""
    try:
        clean_text = text.replace("*", "").replace("#", "").strip()
        if not clean_text:
            return False
            
        tts = gTTS(
            text=clean_text,
            lang="vi",
            slow=False,
            tld="com.au"
        )
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            temp_path = tmp_file.name
        
        pygame.mixer.quit()
        pygame.mixer.pre_init(frequency=88400, size=-16, channels=2, buffer=1024)
        pygame.mixer.init()
        
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        
        pygame.mixer.music.stop()
        os.unlink(temp_path)
        
        return True
        
    except Exception as e:
        st.error(f"🔊 Lỗi fallback TTS: {e}")
        return False

def process_response_tone(response_text):
    """Add gentle tone markers to the response"""
    gentle_response = response_text.replace("*", "")
    return gentle_response

def encode_image_for_gemini(image):
    """Convert PIL Image to base64 for Gemini"""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

def analyze_image_with_zizou(image, user_question="", personality="professional"):
    """Analyze image using Gemini with selected personality"""
    try:
        # Convert image to base64
        image_data = encode_image_for_gemini(image)
        
        # Prepare prompt
        if user_question:
            prompt = f"Hãy phân tích hình ảnh này và trả lời câu hỏi: {user_question}"
        else:
            prompt = "Hãy mô tả và phân tích hình ảnh này một cách chi tiết bằng tiếng Việt."
        
        # Send to Gemini with image
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": image_data
                            }
                        }
                    ]
                }
            ],
            config=types.GenerateContentConfig(
                temperature=0.8,
                system_instruction=PERSONALITY_CONFIGS[personality]["prompt"]
            )
        )
        
        return response.text
        
    except Exception as e:
        return f"Xin lỗi, có lỗi khi phân tích hình ảnh: {str(e)}"

def get_zizou_response(user_input, personality="professional"):
    """Generate response with selected personality"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=user_input,
            config=types.GenerateContentConfig(
                temperature=0.8,
                system_instruction=PERSONALITY_CONFIGS[personality]["prompt"]
            )
        )
        return response.text
        
    except Exception as e:
        print(f"API Error: {e}")
        return "Xin lỗi bạn, có chút vấn đề kỹ thuật. Bạn có thể thử lại không?"

def analyze_file_content(file_content, file_name, user_question="", personality="professional"):
    """Analyze file content with Zizou"""
    try:
        prompt = f"Phân tích file '{file_name}' với nội dung:\n\n{file_content[:3000]}"
        if len(file_content) > 3000:
            prompt += "\n\n[File bị cắt ngắn do quá dài]"
        
        if user_question:
            prompt += f"\n\nCâu hỏi cụ thể: {user_question}"
        
        response = get_zizou_response(prompt, personality)
        return process_response_tone(response)
        
    except Exception as e:
        return f"Lỗi phân tích file: {str(e)}"

# Streamlit interface
def streamlit_interface():
    # Header with status indicator
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1>🤖 Zizou AI Assistant</h1>
        <div style="display: flex; align-items: center; justify-content: center; margin-top: 1rem;">
            <span class="status-online"></span>
            <span style="color: #ecf0f1; font-size: 1.1rem; font-weight: 500;">Online & Ready to Help</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown('<div class="sidebar-header"><h2>🎛️ Cấu hình</h2></div>', unsafe_allow_html=True)
        
        # Personality selection
        st.markdown("### 🎭 Tính cách AI")
        personality = st.selectbox(
            "Chọn phong cách trả lời:",
            options=list(PERSONALITY_CONFIGS.keys()),
            format_func=lambda x: PERSONALITY_CONFIGS[x]["name"],
            index=0,
            help="Chọn cách Zizou sẽ trả lời bạn"
        )
        
        # Voice selection
        st.markdown("### 🔊 Cấu hình giọng nói")
        voice_option = st.selectbox(
            "Chọn giọng nói:",
            options=list(VOICE_OPTIONS.keys()),
            index=0,
            format_func=lambda x: f"{x}",
            help="Chọn giọng nói cho Zizou"
        )
        
        # Display voice description
        st.info(f"ℹ️ {VOICE_OPTIONS[voice_option]['description']}")
        
        # Volume control
        st.markdown("### 🎚️ Âm lượng")
        volume = st.slider("Âm lượng:", 0, 100, 80, help="Điều chỉnh âm lượng phát")
        
        # Stats
        st.markdown("### 📊 Thống kê")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Phiên", "1", delta="Active")
        with col2:
            st.metric("Trạng thái", "Online", delta="✅")
    
    # Store configurations in session state
    st.session_state.personality = personality
    st.session_state.voice_option = voice_option
    st.session_state.volume = volume / 100
    
    # Create tabs with enhanced styling
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🖼️ Hình ảnh", "📁 File", "🎤 Voice"])
    
    with tab1:
        st.markdown("### 💬 Trò chuyện với Zizou")
        
        # Chat input
        user_input = st.text_area(
            "Nhập câu hỏi:", 
            height=120, 
            placeholder="Hỏi Zizou bất cứ điều gì... 🤔",
            key="chat_input"
        )
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            if st.button("🚀 Gửi câu hỏi", type="primary", use_container_width=True):
                if user_input:
                    with st.spinner("🤔 Zizou đang suy nghĩ..."):
                        response = get_zizou_response(user_input, personality)
                        response = process_response_tone(response)
                        
                        # Display conversation in chat format
                        st.markdown(f'<div class="user-message">👤 <strong>Bạn:</strong><br>{user_input}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="assistant-message">🤖 <strong>Zizou ({PERSONALITY_CONFIGS[personality]["name"]}):</strong><br>{response}</div>', unsafe_allow_html=True)
                        
                        st.session_state.last_response = response
                else:
                    st.warning("⚠️ Vui lòng nhập câu hỏi!")
        
        with col2:
            if st.button("🔊 Nghe câu trả lời", use_container_width=True):
                if hasattr(st.session_state, 'last_response'):
                    with st.spinner("🎵 Đang phát âm thanh..."):
                        voice_info = VOICE_OPTIONS[voice_option]
                        if voice_info["model"] == "gtts":
                            success = speak_with_gtts_fallback(st.session_state.last_response)
                        else:
                            success = speak_with_gemini_voice(st.session_state.last_response, voice_info["voice"])
                        
                        if success:
                            st.success("✅ Đã phát xong!")
                        else:
                            st.error("❌ Không thể phát âm thanh")
                else:
                    st.warning("⚠️ Chưa có câu trả lời để phát!")
        
        with col3:
            if st.button("🗑️ Xóa", use_container_width=True):
                if 'last_response' in st.session_state:
                    del st.session_state.last_response
                st.rerun()
    
    with tab2:
        st.markdown("### 🖼️ Phân tích hình ảnh")
        
        uploaded_image = st.file_uploader(
            "📷 Tải lên hình ảnh:",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            help="Zizou sẽ phân tích và giải thích hình ảnh"
        )
        
        image_question = st.text_input(
            "❓ Câu hỏi về hình ảnh:",
            placeholder="VD: Trong hình này có gì? Giải thích chi tiết...",
            key="image_question"
        )
        
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(image, caption="📷 Hình ảnh đã tải lên", use_column_width=True)
            
            with col2:
                st.markdown('<div class="stColumn">', unsafe_allow_html=True)
                if st.button("🔍 Phân tích hình ảnh", type="primary", use_container_width=True):
                    with st.spinner("🔎 Zizou đang phân tích..."):
                        analysis = analyze_image_with_zizou(image, image_question, personality)
                        
                        st.markdown(f"**🤖 Phân tích của Zizou ({PERSONALITY_CONFIGS[personality]['name']}):**")
                        st.write(analysis)
                        
                        st.session_state.last_image_response = analysis
                
                if st.button("🔊 Nghe phân tích", use_container_width=True):
                    if hasattr(st.session_state, 'last_image_response'):
                        with st.spinner("🎵 Đang phát âm thanh..."):
                            voice_info = VOICE_OPTIONS[voice_option]
                            if voice_info["model"] == "gtts":
                                success = speak_with_gtts_fallback(st.session_state.last_image_response)
                            else:
                                success = speak_with_gemini_voice(st.session_state.last_image_response, voice_info["voice"])
                            
                            if success:
                                st.success("✅ Đã phát xong!")
                    else:
                        st.warning("⚠️ Chưa có phân tích để phát!")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 📁 Phân tích File")
        
        uploaded_files = st.file_uploader(
            "📄 Tải lên file:",
            type=['txt', 'py', 'html', 'css', 'js', 'json', 'csv'],
            accept_multiple_files=True,
            help="Zizou có thể đọc và phân tích code, text files"
        )
        
        file_question = st.text_input(
            "❓ Câu hỏi về file:",
            placeholder="VD: Code này làm gì? Tóm tắt nội dung...",
            key="file_question"
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                st.markdown(f"""
                <div class="stColumn">
                    <h4>📄 File: {uploaded_file.name}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    try:
                        # Read file content
                        file_content = uploaded_file.read().decode("utf-8")
                        
                        # Show preview based on file type
                        if uploaded_file.name.endswith(('.py', '.html', '.css', '.js', '.json')):
                            st.code(file_content[:800] + "..." if len(file_content) > 800 else file_content)
                        else:
                            st.text_area(f"Nội dung preview:", file_content[:500] + "..." if len(file_content) > 500 else file_content, height=200, key=f"preview_{uploaded_file.name}")
                        
                        # Reset file pointer for analysis
                        uploaded_file.seek(0)
                        
                    except Exception as e:
                        st.error(f"❌ Không thể đọc file: {e}")
                        continue
                
                with col2:
                    st.markdown('<div class="stColumn">', unsafe_allow_html=True)
                    st.markdown("**🔧 Thao tác:**")
                    
                    if st.button(f"🔍 Phân tích", key=f"analyze_{uploaded_file.name}", use_container_width=True):
                        with st.spinner(f"📖 Đang phân tích {uploaded_file.name}..."):
                            try:
                                uploaded_file.seek(0)
                                file_content = uploaded_file.read().decode("utf-8")
                                analysis = analyze_file_content(file_content, uploaded_file.name, file_question, personality)
                                
                                st.markdown(f"**🤖 Phân tích của Zizou ({PERSONALITY_CONFIGS[personality]['name']}):**")
                                st.write(analysis)
                                
                                st.session_state[f'file_response_{uploaded_file.name}'] = analysis
                                
                            except Exception as e:
                                st.error(f"❌ Lỗi: {e}")
                    
                    response_key = f'file_response_{uploaded_file.name}'
                    if st.button(f"🔊 Nghe", key=f"voice_{uploaded_file.name}", use_container_width=True):
                        if response_key in st.session_state:
                            with st.spinner("🎵 Đang phát..."):
                                voice_info = VOICE_OPTIONS[voice_option]
                                if voice_info["model"] == "gtts":
                                    success = speak_with_gtts_fallback(st.session_state[response_key])
                                else:
                                    success = speak_with_gemini_voice(st.session_state[response_key], voice_info["voice"])
                                
                                if success:
                                    st.success("✅ Phát xong!")
                        else:
                            st.warning("⚠️ Chưa có phân tích!")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
    
    with tab4:
        st.markdown("### 🎤 Voice Chat")
        
        # Voice chat status
        if 'voice_chat_active' not in st.session_state:
            st.session_state.voice_chat_active = False
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if not st.session_state.voice_chat_active:
                if st.button("🎤 Bắt đầu Voice Chat", type="primary", use_container_width=True):
                    st.session_state.voice_chat_active = True
                    st.rerun()
            else:
                if st.button("⏹️ Dừng Voice Chat", type="secondary", use_container_width=True):
                    st.session_state.voice_chat_active = False
                    st.rerun()
        
        with col2:
            # Test voice button
            if st.button("🔊 Test giọng nói", use_container_width=True):
                voice_info = VOICE_OPTIONS[voice_option]
                test_text = f"Xin chào! Tôi là Zizou với giọng nói {voice_info['voice'] if voice_info['model'] != 'gtts' else 'tiếng Việt'}. Tôi sẵn sàng giúp đỡ bạn!"
                
                with st.spinner("🎵 Đang test giọng nói..."):
                    if voice_info["model"] == "gtts":
                        success = speak_with_gtts_fallback(test_text)
                    else:
                        success = speak_with_gemini_voice(test_text, voice_info["voice"])
                    
                    if success:
                        st.success("✅ Giọng nói hoạt động tốt!")
                    else:
                        st.error("❌ Có vấn đề với giọng nói")
        
        with col3:
            # Voice settings
            if st.button("⚙️ Cài đặt", use_container_width=True):
                st.info(f"""
                **🎛️ Cấu hình hiện tại:**
                - Tính cách: {PERSONALITY_CONFIGS[personality]['name']}
                - Giọng nói: {voice_option}
                - Âm lượng: {int(st.session_state.volume * 100)}%
                """)
        
        # Voice chat interface
        if st.session_state.voice_chat_active:
            st.markdown("""
            <div style="background: linear-gradient(45deg, rgba(46, 204, 113, 0.2), rgba(52, 152, 219, 0.2)); 
                        border-radius: 15px; padding: 20px; margin: 20px 0; text-align: center;">
                <div class="voice-wave">
                    <span></span><span></span><span></span><span></span>
                </div>
                <h3>🎤 Voice Chat Đang Hoạt Động!</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Manual voice input simulation
            st.markdown("**🎙️ Voice Input Simulation:**")
            voice_input = st.text_input("Nhập tin nhắn (giả lập voice input):", key="voice_sim", placeholder="Nói điều gì đó với Zizou...")
            
            if st.button("🗣️ Gửi (giả lập voice)", key="send_voice", use_container_width=True):
                if voice_input:
                    with st.spinner("🤔 Zizou đang nghe và trả lời..."):
                        # Get response
                        response = get_zizou_response(voice_input, personality)
                        response = process_response_tone(response)
                        
                        # Show conversation in chat bubbles
                        st.markdown(f'<div class="user-message">👤 <strong>Bạn nói:</strong><br>{voice_input}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="assistant-message">🤖 <strong>Zizou ({PERSONALITY_CONFIGS[personality]["name"]}):</strong><br>{response}</div>', unsafe_allow_html=True)
                        
                        # Auto-play response with selected voice
                        with st.spinner(f"🎵 Zizou đang nói với giọng {voice_option}..."):
                            voice_info = VOICE_OPTIONS[voice_option]
                            if voice_info["model"] == "gtts":
                                speak_with_gtts_fallback(response)
                            else:
                                speak_with_gemini_voice(response, voice_info["voice"])
                            st.success("✅ Zizou đã trả lời!")
            
            # Enhanced info box
            st.markdown(f"""
            <div style="background: rgba(52, 152, 219, 0.1); border-radius: 15px; padding: 20px; margin: 20px 0;">
                <h4>📋 Hướng dẫn Voice Chat:</h4>
                <ul style="color: #ecf0f1;">
                    <li>🎯 Nhập tin nhắn vào ô bên trên (giả lập voice input)</li>
                    <li>🚀 Click "Gửi" để Zizou trả lời</li>
                    <li>🔊 Zizou sẽ tự động nói câu trả lời với giọng <strong>{voice_option}</strong></li>
                    <li>🎭 Phong cách trả lời: <strong>{PERSONALITY_CONFIGS[personality]['name']}</strong></li>
                </ul>
                
                <h4>💡 Để sử dụng microphone thực:</h4>
                <p style="color: #bdc3c7;">Chạy script trong terminal: <code>python test.py</code></p>
                
                <h4>🎵 {voice_option} Features:</h4>
                <p style="color: #ecf0f1;">{VOICE_OPTIONS[voice_option]['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Voice chat info when inactive
            st.markdown("""
            <div style="background: rgba(52, 73, 94, 0.3); border-radius: 15px; padding: 30px; text-align: center;">
                <h3>🎤 Voice Chat Features</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px;">
                    <div style="background: rgba(46, 204, 113, 0.1); padding: 15px; border-radius: 10px;">
                        <h4>🎯 Nhận diện giọng nói</h4>
                        <p>Hỗ trợ tiếng Việt và nhiều ngôn ngữ khác</p>
                    </div>
                    <div style="background: rgba(52, 152, 219, 0.1); padding: 15px; border-radius: 10px;">
                        <h4>🔊 Multi-Voice TTS</h4>
                        <p>5+ giọng nói AI chất lượng cao</p>
                    </div>
                    <div style="background: rgba(155, 89, 182, 0.1); padding: 15px; border-radius: 10px;">
                        <h4>🎭 Đa tính cách</h4>
                        <p>4 phong cách trả lời khác nhau</p>
                    </div>
                    <div style="background: rgba(230, 126, 34, 0.1); padding: 15px; border-radius: 10px;">
                        <h4>🤖 AI thông minh</h4>
                        <p>Đối thoại tự nhiên với Gemini AI</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Requirements section
            with st.expander("🔧 Yêu cầu kỹ thuật", expanded=False):
                st.code("""
# Cài đặt thư viện cần thiết:
pip install gtts pygame google-generativeai speechrecognition streamlit pillow pyaudio wave

# Chạy ứng dụng:
streamlit run your_app.py

# Voice chat thực với microphone:
python your_app.py
                """, language="bash")

# Console version for real voice chat
def main_console():
    """Console version with real microphone support and multiple voices"""
    print("🤖 Zizou đang khởi động với đa giọng nói AI... Xin chào bạn!")
    print("💡 Tip: Nói 'tạm biệt' hoặc 'bye' để thoát")
    print("🔊 Voice: Sử dụng Gemini AI voices chất lượng cao")
    
    # Voice selection in console
    print("\n🎵 Chọn giọng nói:")
    voices = list(VOICE_OPTIONS.keys())
    for i, voice in enumerate(voices):
        print(f"{i+1}. {voice} - {VOICE_OPTIONS[voice]['description']}")
    
    try:
        voice_choice = int(input("Chọn giọng nói (1-5): ")) - 1
        if 0 <= voice_choice < len(voices):
            selected_voice = voices[voice_choice]
            print(f"✅ Đã chọn: {selected_voice}")
        else:
            selected_voice = "Kore (Gemini TTS)"
            print(f"⚠️ Lựa chọn không hợp lệ, sử dụng mặc định: {selected_voice}")
    except:
        selected_voice = "Kore (Gemini TTS)"
        print(f"⚠️ Sử dụng giọng mặc định: {selected_voice}")
    
    # Personality selection
    print("\n🎭 Chọn tính cách:")
    personalities = list(PERSONALITY_CONFIGS.keys())
    for i, personality in enumerate(personalities):
        print(f"{i+1}. {PERSONALITY_CONFIGS[personality]['name']}")
    
    try:
        personality_choice = int(input("Chọn tính cách (1-4): ")) - 1
        if 0 <= personality_choice < len(personalities):
            selected_personality = personalities[personality_choice]
            print(f"✅ Đã chọn: {PERSONALITY_CONFIGS[selected_personality]['name']}")
        else:
            selected_personality = "professional"
            print(f"⚠️ Lựa chọn không hợp lệ, sử dụng mặc định: Chuyên nghiệp")
    except:
        selected_personality = "professional"
        print(f"⚠️ Sử dụng tính cách mặc định: Chuyên nghiệp")
    
    print(f"\n🚀 Bắt đầu voice chat với {selected_voice} - {PERSONALITY_CONFIGS[selected_personality]['name']}")
    
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                robot_ear.adjust_for_ambient_noise(mic, duration=1)
                print("🎤 Zizou: Tôi đang lắng nghe...")
                print("⏰ Bạn có 10s để nói!")
                audio = robot_ear.listen(mic, timeout=10, phrase_time_limit=15)
        
            print("🤔 Đang xử lý...")
                
            try:
                you = robot_ear.recognize_google(audio, language="vi-VN")
            except speech_recognition.UnknownValueError:
                error_msg = "😅 Tôi không nghe rõ. Nói lại được không?"
                print(f"🤖 Zizou: {error_msg}")
                voice_info = VOICE_OPTIONS[selected_voice]
                if voice_info["model"] == "gtts":
                    speak_with_gtts_fallback(error_msg)
                else:
                    speak_with_gemini_voice(error_msg, voice_info["voice"])
                continue
            except speech_recognition.RequestError:
                error_msg = "🔧 Có vấn đề kết nối. Thử lại nhé."
                print(f"🤖 Zizou: {error_msg}")
                voice_info = VOICE_OPTIONS[selected_voice]
                if voice_info["model"] == "gtts":
                    speak_with_gtts_fallback(error_msg)
                else:
                    speak_with_gemini_voice(error_msg, voice_info["voice"])
                continue
            
            if not you:
                continue
                
            print(f"👤 Bạn: {you}")
            
            # Exit conditions
            if "tạm biệt" in you.lower() or "bye" in you.lower():
                goodbye_msg = "Tạm biệt! Hẹn gặp lại! 🌟"
                print(f"🤖 Zizou: {goodbye_msg}")
                voice_info = VOICE_OPTIONS[selected_voice]
                if voice_info["model"] == "gtts":
                    speak_with_gtts_fallback(goodbye_msg)
                else:
                    speak_with_gemini_voice(goodbye_msg, voice_info["voice"])
                break
            
            # Generate response
            robot_brain = get_zizou_response(you, selected_personality)
            robot_brain = process_response_tone(robot_brain)
            
            print(f"🤖 Zizou ({PERSONALITY_CONFIGS[selected_personality]['name']}): {robot_brain}")
            
            # Speak with selected voice
            voice_info = VOICE_OPTIONS[selected_voice]
            if voice_info["model"] == "gtts":
                speak_with_gtts_fallback(robot_brain)
            else:
                speak_with_gemini_voice(robot_brain, voice_info["voice"])
            
        except KeyboardInterrupt:
            print("\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    try:
        # Check if running in Streamlit
        streamlit_interface()
    except:
        # Run console version
        main_console()
