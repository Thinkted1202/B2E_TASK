# B2E_TASK
Implement an URL shortener service

### 環境
* OS:CentOS 7
* Code : Python Flask
* Web Server : Gunicorn 
* R-PROXY Server : Nginx
* Cache Server : Redis
* DB Server : Mysql
  
### 分析需求

1. 產生短網址 - API Service  
  1.1. 認證API :  透過帳號密碼認證後，取得Token訪問接下來的API  
  ``http --auth demo@gmail.com:1qaz2wsx  --json POST http://python.thinkted.com.tw/api/v1/tokens/``   
  1.2. 短網址API : 實際產生短網址的 API  
  1.3 區分版本號為 api/v1   
2. 使用短網址 - Web Service  
		2.1 須注意高並發機制  
		2.2 Server Warm Up 機制 

### 系統初擬架構 

針對 高並發機制如下
1. CDN 做為第一層Cache，須開啟Forward機制  
2. Nginx R-Proxy 為第二層Cache 機制，配以Nginx 驅動的 LBS，分散Request量  
	2.1 視需求量體，可改為支援度更高的R-Proxy Server (Varnish Cluster) 
3. 避免大量直接訪問DB，中間做第三層Redis Cache   
  3.1 視需求量體，可以做Redis 的 Cluster 但需要注意 RedisLock 的問題。  
4. Mysql Connection 在做高並發時會是瓶頸，使用Master/Slave機制分流。  
	 4.1 ProxySql 可調節讀寫分流，避免程式端直接誤用Master/Slave 分流  
	4.2 視需求量體，可以將Master Write使用Queue寫入，可以再次緩衝Mysql的Connection數  
	4.3 視需求量體 若考慮到HA機制，可改為DRBD 或 Galera Cluster 
5. 需設定好Warm Up 機制，若主機須重開機情況下，大量Request在第一次會直接訪問到DB  
	5.1 在Nginx開機前，須將Data以Queue的方式餵入Redis  

![Alt text](https://lh3.googleusercontent.com/HuFpKFpFdjlsw_LGmk8dQGMIhF_RqJsHqgFYrhlMW_nJaYun_gyMEvLkyNOej2x-ieLvjylBR4gHbVHuDAA-FpdXrg51K8TT00aWaBTPo9fH1roKB_ggUOOy3Wg8BhaJHTe3soZJUjMIaUt5G7HiaqU3gmImuup8HwpH4YzMVFnPtMmlNfFuCItFvTJbh3Ldap0999I_jzx4c8VFL0R7OI4A_Ol9fZ5xqUKReQF9_Y41QXqE7DGP_G3SEej_QNEP4t643yshzr5cvxxbjDRXNMWuOhIqJ_rImdRkR-GcjiQxjHwabsxstMaQGH5VAUXwswghkt8Kxt0kSNUIl-uIHfjzkrnX_avX-5QYkrQtTcjQvqlu1_CDZNesIFDi3cVsYTbF8IeWLIXiK5n8liUFxMXbO2W7Bw2e4UYjGvkeE0oFK1Cp66pzPiiBLVk1-eUnSiqSemh7iOFnxBl8QKYtTgCPRhhw8viAlg2XHEgQN0x7qYS1dQsaDm0f_el2nAle-bBRFlCNWzf-sYq2xfQuvl63OzCJN2ckus-qJGB6Khk1cR6TYc2uAQZwUD_ckzFEnQdIXZ6boVcwqxDhidsC_50ut6hiXGATCDjQGdGbWGFBw7SkrSTWOJ_ah_vgBYQTawjmV3G0VQaDxDj-C_tKDrXFp0_XrkzO1RdJemfKyPSF--0LtZR6PUD4c1OWxQ=w1400-h442-no)

  
