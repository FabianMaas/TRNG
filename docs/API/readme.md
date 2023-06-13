# REST API Documentation
---

In the context of the documentation we run our rest api on http://localhost:8080.<br>
For productive operation https://\<ip\>:443 should be used.

---

## /
`Redirects to the TRNG page.`

| Methode | URL                            | Header                         |
|---------|--------------------------------|--------------------------------|
| GET     | http://localhost:8080/         | Content-Type: application/json |

- <strong>Request</strong>

  ```text
  GET / HTTP/1.1
  Host: localhost:8080
  Upgrade-Insecure-Requests: 1
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36
  Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
  Sec-Fetch-Site: none
  Sec-Fetch-Mode: navigate
  Sec-Fetch-User: ?1
  Sec-Fetch-Dest: document
  sec-ch-ua: 
  sec-ch-ua-mobile: ?0
  sec-ch-ua-platform: ""
  Accept-Encoding: gzip, deflate
  Accept-Language: en-US,en;q=0.9
  Cookie: themePreference=dark
  Connection: close
  ```

- <strong>Response</strong>

  ```text
  HTTP/1.1 301 MOVED PERMANENTLY
  Server: Werkzeug/2.3.4 Python/3.11.3
  Date: Tue, 13 Jun 2023 09:19:37 GMT
  Content-Type: text/html; charset=utf-8
  Content-Length: 197
  Location: /trng
  Connection: close

  <!doctype html>
  <html lang=en>
  <title>Redirecting...</title>
  <h1>Redirecting...</h1>
  <p>You should be redirected automatically to the target URL: <a href="/trng">/trng</a>. If not, click the link.
  ```

---

## /trng

---

## /trng/randomNum/init

---

## /trng/randomNum/shutdown

---

## /trng/randomNum/getRandom

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```
