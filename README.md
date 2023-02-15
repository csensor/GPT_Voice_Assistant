https://user-images.githubusercontent.com/7485678/219089373-18906d4f-a5ab-4a92-936b-ee8126028525.mov
# GPT_Voice_Assistant
基于openAI GPT实现的智能交互语音助手,产品主要涉及四个任务：语音唤醒，语音识别，GPT对话，文本转语音

# 实现的功能
通过唤醒词唤醒后，进行语音对话

# 可玩性
1. 可在PC（笔记本、台式机）实现语音助手功能
2. 运行在树莓派（Raspberry Pi）增加麦克风+喇叭可实现完整语音助手功能

# 安装方法
1. `pip install -r requirements.txt`

# 配置
按需修改配置
```
{
    "porcupine": {
        "access_key": "",                // porcupine的ak
        "keywords": [],                  // 可使用 porcupine 内置的唤醒词，否则使用keyword_paths
        "keyword_paths": ["ppn/hello-model_en_windows_v2_1_0.ppn"], // 项目下自带了唤醒词模型，在resource/ppn 目录下可供选择
        "sensitivities": [0.5]           // 唤醒词阈值，值越高precision越高，反之recall越高
    },
    "nlp_service": {
        "paddlepaddle": {               
            "asr_url": "http://x.x.x.x:8090/paddlespeech/asr",  // 自己搭建的paddlespeech的asr服务, x 换成ip地址
            "tts_url": "http://x.x.x.x:8090/paddlespeech/tts"   // 自己搭建的paddlespeech的tts服务, x 换成ip地址
        }
    },
    "openai": {
        "api_key": "xxxxxxxxxxxx" // openai 上的api key
    } 
}
```

# 运行方法
1. `python3 gva.py`

# 常见问题
> 如何生成自己的唤醒词？

见 https://console.picovoice.ai/

> 如何搭建paddlespeech 服务

见 https://github.com/PaddlePaddle/PaddleSpeech

> 安装依赖时报错： "fatal error: portaudio.h: No such file or directory"

`sudo apt install portaudio19-dev` 可解决
