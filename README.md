# Django REST Framework 예제 프로젝트

이 프로젝트는 Django REST Framework의 주요 10가지 기능을 학습하고 구현한 예제입니다.

---

## 전체 흐름 다이어그램

```
[사용자 요청]
  ↓
[URL → Router → ViewSet]
  ↓
[permissions 검사 + queryset 구성]
  ↓
[filtering, ordering, pagination]
  ↓
[Serializer로 변환]
  ↓
[Response로 응답 반환 + Swagger에서 시각화]
```

---

## 주요 기능 요약

| 번호 | 기능 | 설명 |
|------|------|------|
| 1 | Serialization | 모델을 JSON으로 변환 (ModelSerializer, HyperlinkedSerializer) |
| 2 | Request & Response | API 요청/응답 처리 (ViewSet, APIView) |
| 3 | Class-based Views | APIView, ModelViewSet 기반 구조 |
| 4 | Authentication & Permissions | 토큰 인증, 작성자 권한 처리 |
| 5 | Relationships & Hyperlinked APIs | URL 기반 관계 필드 연결 |
| 6 | Viewsets & Routers | URL 자동 라우팅 |
| 7 | Throttling | 요청 제한 처리 (UserRateThrottle) |
| 8 | Filtering & Ordering | 쿼리 파라미터 기반 검색 및 정렬 |
| 9 | Pagination | 페이지 단위 응답 처리 (PageNumberPagination) |
| 10 | Swagger | API 문서 자동 생성 (drf-spectacular) |

---

## 설치 및 실행

```bash
git clone https://github.com/yourname/drf-example.git
cd drf-example

# 가상환경 설정
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 마이그레이션 및 관리자 계정 생성
python manage.py migrate
python manage.py createsuperuser

# 서버 실행
python manage.py runserver
```

---

## 핵심 개념 정리

### 1. ModelSerializer vs HyperlinkedModelSerializer

| 항목 | ModelSerializer | HyperlinkedModelSerializer |
|------|------------------|-----------------------------|
| 기본 구조 | id 기반 | url 기반 |
| 관계 표현 | 정수 ID로 참조 | 하이퍼링크(URL)로 참조 |
| 직관성 | 간단하지만 탐색 어려움 | RESTful하고 프론트 친화적 |
| 예시 | "author": 1 | "author": "http://.../users/1/" |

- ModelSerializer는 관계를 숫자 ID로 표현
- HyperlinkedModelSerializer는 관계를 URL 링크로 표현
- RESTful한 구조 설계를 위한 Hypermedia(HATEOAS) 원칙 적용

### 2. view_name

- DRF ViewSet은 내부적으로 view_name을 가짐
- 예시:
  - post-list → `/api/posts/`
  - post-detail → `/api/posts/<pk>/`
- Hyperlinked 필드에서 참조할 URL 이름 지정 시 사용

```python
view_name = 'post-detail'
```

### 3. basename

- DRF 라우터가 view_name을 생성할 때 사용하는 기준 단어
- 예시:

```python
router.register('posts', PostViewSet, basename='post')
```

- 생성되는 view_name: post-list, post-detail
- 하이퍼링크 필드에서 참조될 이름 체계가 됨

### 4. permissions

| 권한 클래스 | 설명 |
|-------------|------|
| IsAuthenticatedOrReadOnly | 로그인한 사용자만 쓰기 가능 |
| IsAuthorOrReadOnly | 객체의 작성자만 수정/삭제 가능 |

- 인증 여부와 작성자 여부에 따라 요청 제어 가능

### 5. filterset_fields, ordering_fields

- 검색/정렬 기능을 위한 쿼리 파라미터 지원
- 예시:

```
GET /api/posts/?author__username=alice&ordering=-created
```

- filterset_fields: 검색 필드 지정
- ordering_fields: 정렬 필드 지정

### 6. drf-spectacular

- Swagger 기반의 자동 API 문서 생성 도구
- 주요 경로:
  - `/schema/` → OpenAPI JSON 문서
  - `/docs/` → Swagger UI

- 요청/응답 구조, 필드 설명, 예시 등을 시각화 가능

---

## Django REST Framework 작동 흐름

이 프로젝트에서 구현된 기능은 다음과 같은 순서로 작동합니다.

### 1. URL 요청

- 사용자가 `/api/posts/` 등으로 요청을 보냄
- urls.py에서 router.register()를 통해 ViewSet으로 연결됨

### 2. View 또는 ViewSet 처리

- ViewSet 또는 APIView가 요청을 수신
- 요청 메서드(GET, POST, PATCH 등)에 따라 메서드 자동 분기
- permission_classes를 통해 인증/권한 검사 수행

### 3. 권한 확인

- TokenAuthentication으로 인증 수행
- IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly 등 권한 제어

### 4. QuerySet 필터링 및 페이지 분할

- filterset_fields와 ordering_fields에 따라 필터링/정렬 처리
- 페이지네이션(PageNumberPagination) 설정에 따라 결과 분할

### 5. Serializer를 통한 JSON 변환

```python
serializer.save()   # DB 저장
serializer.data     # JSON 반환
```

- ModelSerializer 또는 HyperlinkedModelSerializer 사용

### 6. Response 반환

- Response(serializer.data) 형태로 응답 반환
- 상태 코드, pagination, 헤더 포함

### 7. drf-spectacular 문서 자동 생성

- 각 API의 요청/응답 구조를 자동 문서화
- Swagger UI(`/docs/`)에서 직접 테스트 가능
- [http://localhost:8000/docs/](http://localhost:8000/docs/)
---

이 문서는 Django REST Framework의 기능을 구조적으로 학습하고,  
실제 RESTful API를 구현하는 데 필요한 설계 흐름을 이해하기 위한 안내서입니다.
