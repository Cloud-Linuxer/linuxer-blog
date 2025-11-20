# CloudFront 설정 가이드

## 문제
Hugo는 `/posts/slug/index.html` 구조로 생성하지만, CloudFront는 `/posts/slug/` 요청 시 자동으로 `index.html`을 찾지 않습니다.

## 해결 방법 (CloudFront Function 사용)

### 1. CloudFront Function 생성

AWS Console → CloudFront → Functions → Create function

**Function 이름**: `index-rewrite`

**코드**:
```javascript
function handler(event) {
    var request = event.request;
    var uri = request.uri;

    // URI가 /로 끝나면 index.html 추가
    if (uri.endsWith('/')) {
        request.uri += 'index.html';
    }
    // 파일 확장자가 없으면 /index.html 추가
    else if (!uri.includes('.')) {
        request.uri += '/index.html';
    }

    return request;
}
```

### 2. Function 연결

1. CloudFront → Distributions → 본인의 distribution 선택
2. Behaviors → Default (*) → Edit
3. Function associations:
   - **Viewer request**: `index-rewrite` 선택
4. Save changes

### 3. 테스트

배포 후 (5-10분 소요) 다음 URL들이 모두 작동해야 합니다:
- ✅ `https://hugo.linuxer.name/posts/gpt-oss-20b-tool-calling/`
- ✅ `https://hugo.linuxer.name/posts/gpt-oss-20b-tool-calling/index.html`

## 대안: Lambda@Edge (고급)

더 복잡한 리다이렉션이 필요하면 Lambda@Edge를 사용할 수 있습니다.

```javascript
exports.handler = async (event) => {
    const request = event.Records[0].cf.request;
    const uri = request.uri;

    if (uri.endsWith('/')) {
        request.uri += 'index.html';
    } else if (!uri.includes('.')) {
        request.uri += '/index.html';
    }

    return request;
};
```

## 참고

- CloudFront Function: 무료, 빠름, 간단한 리라이트
- Lambda@Edge: 유료, 복잡한 로직 가능, 느림

**권장**: CloudFront Function 사용
