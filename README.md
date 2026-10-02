# 💬 AI 챗봇 앱

휴대폰에서 바로 쓸 수 있는 Claude 기반 챗봇 앱입니다 (Streamlit).

- 대화형 채팅 화면, 실시간(스트리밍) 답변
- 챗봇 성격 선택: 만능 도우미 / 우리반 도우미 / 공부 친구 (시스템 프롬프트 직접 수정 가능)
- 휴대폰 화면에 맞춘 레이아웃

## 실행 방법

1. 패키지 설치

   ```
   $ pip install -r requirements.txt
   ```

2. API 키 설정 — `.streamlit/secrets.toml` 파일을 만들고 아래처럼 적습니다 (이 파일은 git에 올라가지 않습니다).

   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```

   또는 환경 변수 `ANTHROPIC_API_KEY`를 설정하거나, 앱 사이드바에 직접 입력해도 됩니다.

3. 실행

   ```
   $ streamlit run streamlit_app.py
   ```

## 휴대폰에서 앱처럼 쓰기

1. [Streamlit Community Cloud](https://share.streamlit.io)에 이 저장소를 배포하고, 앱 설정의 **Secrets**에 `ANTHROPIC_API_KEY`를 넣습니다.
2. 휴대폰 브라우저로 앱 주소를 엽니다.
3. **iPhone(Safari)**: 공유 → "홈 화면에 추가" / **Android(Chrome)**: ⋮ 메뉴 → "홈 화면에 추가"

이제 홈 화면 아이콘을 눌러 앱처럼 사용할 수 있습니다.
