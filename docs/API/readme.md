# REST API Documentation
---

In the context of the documentation we run our rest api on http://localhost:8080.<br>
For productive operation https://\<ip\>:443 should be used.

---
<strong>Endpoints:</strong>
  <ol>
    <li><a href="#">/</a></li>
    <li><a href="#trng">/trng</a></li>
    <li><a href="#trngrandomnuminit">/trng/randomNum/init</a></li>
    <li><a href="#trngrandomnumshutdown">/trng/randomNum/shutdown</a></li>
    <li><a href="#trngrandomnumgetrandom">/trng/randomNum/getRandom</a></li>
    <li><a href="#trnggetcount">/trng/getCount</a></li>
  </ol>

---

## /
`Redirects to the TRNG page.`

| Method  | URL                            | Header                         |
|---------|--------------------------------|--------------------------------|
| GET     | http://localhost:8080/         | Accept: text/html              |

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

  ```html
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
`Renders the TRNG page.`

| Method  | URL                            | Header                         |
|---------|--------------------------------|--------------------------------|
| GET     | http://localhost:8080/trng     | Accept: text/html              |

- <strong>Request</strong>

  ```text
  GET /trng HTTP/1.1
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
  Referer: http://localhost:8080/
  ```

- <strong>Response</strong>

  ```html
  HTTP/1.1 200 OK
  Server: Werkzeug/2.3.4 Python/3.11.3
  Date: Tue, 13 Jun 2023 10:17:04 GMT
  Content-Type: text/html; charset=utf-8
  Content-Length: 1949
  Connection: close

  <!DOCTYPE html>
  <html>

  <head>
    <meta charset="UTF-8" />
    <title>TRNG WaveTech</title>
    <link rel="shortcut icon" href="static/img/logo.png" />
    <link rel="stylesheet" type="text/css" href="static/css/main.css" />
  </head>

  <body>
    <canvas id="canvas" hidden="true"></canvas>
    <div class="container content">

      <h1>True Random Number Generator</h1>

      <img src="static/img/logo.png" style="max-width: 200px; max-height: auto; margin-bottom: 20px;" alt="logo_wavetech" />

      <div class="toggle-container">
        <span class="toggle-label">Light/Dark</span>
        <div class="toggle-btn" onclick="toggleTheme()"></div>
      </div>

      <div>
        <button id="toggleBtn" class="button">Start</button>
      </div>

      <div>
        <label for="quantity-input">Quantity:</label>
        <input type="number" id="quantity-input" name="quantity" min="1" max="1000" class="my-input" value="1"/>
        <label for="numBits-input">NumBits:</label>
        <input type="number" id="numBits-input" name="numBits" min="1" max="1000" class="my-input" value="1"/>
        <button disabled="true" id="generate-btn" class="button">Generate Random Hex Values</button>
        <button disabled="true" id="export-btn" class="button">Export Random Hex Values</button>
      </div>

      <div id="alertDiv" class="alert" hidden="true"></div>
      <div id="infoAlertDiv" class="alert" hidden="true"></div>

      <div id="loading-spinner" style="display: none;">
        <img src="static/img/spinner.gif" alt="Loading...">
      </div>

      <table id="result-table"></table>

      <footer class="footer-github">
        <p>Made with ❤️ by WaveTech</p>
        <a href="https://github.com/FabianMaas/TRNG"  target="_blank">
          <img id="github-icon" src="static/img/github-mark.png" width="24" height="24" alt="GitHub">
        </a>
      </footer>

    </div>

    <script src="static/js/main.js"></script>
    <script src="static/js/background.js"></script>

  </body>

  </html>
  ```

---

## /trng/randomNum/init
`Initializes the TRNG system.`

| Method  | URL                                       | Header                         |
|---------|-------------------------------------------|--------------------------------|
| GET     | http://localhost:8080/trng/randomNum/init | Accept: \*/\*                  |

- <strong>Request</strong>

  ```text
  GET /trng/randomNum/init HTTP/1.1
  Host: localhost:8080
  sec-ch-ua: 
  sec-ch-ua-mobile: ?0
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36
  sec-ch-ua-platform: ""
  Accept: */*
  Sec-Fetch-Site: same-origin
  Sec-Fetch-Mode: cors
  Sec-Fetch-Dest: empty
  Referer: http://localhost:8080/trng
  Accept-Encoding: gzip, deflate
  Accept-Language: en-US,en;q=0.9
  Cookie: themePreference=dark
  Connection: close
  ```
  
- <strong>Response</strong>

  ```text
  HTTP/1.1 200 OK
  Server: Werkzeug/2.3.4 Python/3.11.3
  Date: Tue, 13 Jun 2023 10:21:38 GMT
  Content-Type: text/html; charset=utf-8
  Content-Length: 90
  Connection: close

  successful operation; random number generator is ready and random numbers can be requested
  ```

---

## /trng/randomNum/shutdown
`Shuts down the TRNG system.`

| Method  | URL                                           | Header                         |
|---------|-----------------------------------------------|--------------------------------|
| GET     | http://localhost:8080/trng/randomNum/shutdown | Accept: \*/\*                  |

- <strong>Request</strong>

  ```text
  GET /trng/randomNum/shutdown HTTP/1.1
  Host: localhost:8080
  sec-ch-ua: 
  sec-ch-ua-mobile: ?0
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36
  sec-ch-ua-platform: ""
  Accept: */*
  Sec-Fetch-Site: same-origin
  Sec-Fetch-Mode: cors
  Sec-Fetch-Dest: empty
  Referer: http://localhost:8080/trng
  Accept-Encoding: gzip, deflate
  Accept-Language: en-US,en;q=0.9
  Cookie: themePreference=dark
  Connection: close
  ```
  
- <strong>Response</strong>

  ```text
  HTTP/1.1 200 OK
  Server: Werkzeug/2.3.4 Python/3.11.3
  Date: Tue, 13 Jun 2023 10:23:43 GMT
  Content-Type: text/html; charset=utf-8
  Content-Length: 76
  Connection: close

  successful operation; random number generator has been set to 'standby mode'
  ```

---

## /trng/randomNum/getRandom
`Retrieves random bits from the database and converts them to HEX encoding.`

| Method  | URL                                            | Query Parameter                         | Header                         | 
|---------|------------------------------------------------|-----------------------------------------|--------------------------------|
| GET     | http://localhost:8080/trng/randomNum/getRandom | quantity(default=1), numBits(default=1) | Accept: \*/\*                  |


- <strong>Request</strong>

  ```text
  GET /trng/randomNum/getRandom?quantity=3&numBits=512 HTTP/1.1
  Host: localhost:8080
  sec-ch-ua: 
  sec-ch-ua-mobile: ?0
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36
  sec-ch-ua-platform: ""
  Accept: */*
  Sec-Fetch-Site: same-origin
  Sec-Fetch-Mode: cors
  Sec-Fetch-Dest: empty
  Referer: http://localhost:8080/trng
  Accept-Encoding: gzip, deflate
  Accept-Language: en-US,en;q=0.9
  Cookie: themePreference=dark
  Connection: close
  ```
  
- <strong>Response</strong>

  ```text
  HTTP/1.1 200 OK
  Server: Werkzeug/2.3.4 Python/3.11.3
  Date: Tue, 13 Jun 2023 10:25:41 GMT
  Content-Type: application/json
  Content-Length: 504
  Connection: close
  ```
  ```json
  {
      "description": "successful operation; HEX-encoded bit arrays (with leading zeros if required)",
      "randomBits": [
          "639112B933906BD05DD3EF6BD33D7B4B4A515AD96AD46667A032C0B3A599C307E4773C8756647718FD6F5DA20CEF782E3C5B285B8A3986E58935041AE67B4DA6",
          "B1654FA4CD60012883E2D70724EC9A9423736C38968F0F1D5DA93273C0B4CF588424EF4F9FB464F385C972CC04CFBF4DF604097C996F0964CAF521C6BF92E9AC",
          "192478EC381182ACFCE7C335A386EBDEC667ED6A16C01A7A5A5D94B25436149F6F56320CDD19AF1127271B2DE706319A242FEEBDB69F8553D6AC85A406C57D1B"
      ]
  }
  ```
  
---

## /trng/getCount
` Retrieves the count of stored random bits from the database.`

| Method  | URL                                            | Header                         |
|---------|------------------------------------------------|--------------------------------|
| GET     | http://localhost:8080/trng/getCount           | Accept: \*/\*                  |


- <strong>Request</strong>

  ```text
  GET /trng/getCount HTTP/1.1
  Host: localhost:8080
  sec-ch-ua: 
  sec-ch-ua-mobile: ?0
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36
  sec-ch-ua-platform: ""
  Accept: */*
  Sec-Fetch-Site: same-origin
  Sec-Fetch-Mode: cors
  Sec-Fetch-Dest: empty
  Referer: http://localhost:8080/trng
  Accept-Encoding: gzip, deflate
  Accept-Language: en-US,en;q=0.9
  Cookie: themePreference=dark
  Connection: close
  ```
  
- <strong>Response</strong>

  ```text
  HTTP/1.1 200 OK
  Server: Werkzeug/2.3.4 Python/3.11.3
  Date: Tue, 13 Jun 2023 10:52:06 GMT
  Content-Type: application/json
  Content-Length: 6
  Connection: close

  18752
  ```
