


# DW3000 超寬頻空間定位安全傳輸系統

[![License](https://img.shields.io/badge/license-Apache_2.0-blue.svg?style=flat-square)](LICENSE) 
![Python](https://img.shields.io/badge/Python-3.13%2B-green.svg?style=flat-square&logo=python&logoColor=white)
![Hardware](https://img.shields.io/badge/Hardware-DW3000%20%7C%20ESP32-blue?style=flat-square&logo=espressif&logoColor=white)
![Framework](https://img.shields.io/badge/Framework-Arduino-orange?style=flat-square&logo=arduino&logoColor=white)
![Security](https://img.shields.io/badge/Security-AES--CCM%20%2B%20STS-red?style=flat-square)

---
`點此處按鈕，可切換語言！！`

[![English](https://img.shields.io/badge/Language-English-blue)](README.md) 
[![繁體中文](https://img.shields.io/badge/Language-繁體中文-green)](README.zh-TW.md)


---

## 📌 關於此系統
本專案使用 `DW3000 超寬頻板` 配合 `Arduino` `Python` `SS-TWR` 實現即時空間定位功能，並具備 `AES-CCM 加密演算法` 與 `安全時間戳 STS`，用以確保定位資料在無線傳輸中的機密性與完整性，打造安全的物聯網空間傳輸系統。

* **系統展示**

| 對稱式雙向測距 SS-TWR | 即時空間定位 |
| :---: | :---: |
| ![ss-twr](Draw_Error_Images/markdown_image/SS_TWR.gif) <br> 透過雙向封包能得知板子相差距離 | ![display_irl](Draw_Error_Images/markdown_image/positioning_display_irl.gif) <br> 透過二維與三維演算法能得知 Tag 位置 |

* **封包格式 (未加密)**

`Poll 封包`
| 欄位 | Mac Header | Seq Num | Pan ID | Tag ShortAdr | Anc ShortAdr | Function | CRC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **長度** | 2B | 1B | 2B | 2B | 2B | 1B | 2B |
| **數值** | `41 88` | `A5` | `CA DE` | `54 31` | `41 31` | `E0` | `FA E4` |
| **說明** | MAC標頭 | 封包序號 | 網路ID | 標籤短網址 | 基站短網址 | 功能碼(Poll) | 錯誤校驗碼 |

`Respone 封包`
| 欄位 | Mac Header | Seq Num | Pan ID | Tag ShortAdr | Anc ShortAdr | Function | T2 poll_rx | T3 resp_tx | CRC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **長度** | 2B | 1B | 2B | 2B | 2B | 1B | 4B | 4B | 2B |
| **數值** | `41 88` | `00` | `CA DE` | `41 31` | `54 31` | `E1` | `59 1A 57 05` | `01 5A 26 09` | `85 2D` |
| **說明** | MAC標頭 | 封包序號 | 網路ID | 標籤短網址 | 基站短網址 | 功能碼(Respone) | 接收時間戳($T_2$) | 發射時間戳($T_3$) | 錯誤校驗碼 |

* **封包格式 (AES-CCM 加密)**

`Poll 封包`
| 欄位 | FCF | Seq Num | Pan ID | Dst_Adr | Src_Adr | Security Control | Frame Counter | Key Index | Payload | MIC | CRC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **長度** | 2B | 1B | 2B | 8B | 8B | 1B | 4B | 1B | 12B | 16B | 2B |
| **數值** | `09 EC` | `D0` | `21 43` | `88 77...11` | `11 22...88` | `0F` | `D0 09 00 00` | `01` | `5D 9B...F5` | `EF 60...CE` | `9D 8E` |
| **說明** | 安全控制 | 封包序號 | 網路ID | 目的長網址 | 來源長網址 | 加密控制位 | 防重放計數器 | 密鑰索引 | AES加密數據 | 訊息認證碼 | 錯誤校驗碼 |

---

## 🌳 檔案結構樹
```bash
📂 UWB_Program_DW3000
┣ 📂 DW3000     # UWB 硬體驅動函式庫
┃  ┣ 📝 dw3000.h                     # 主引入標頭檔
┃  ┣ 📝 dw3000_types.h               # 資料型態定義
┃  ┣ 📝 dw3000_version.h             # 驅動版本
┃  ┣ 📝 dw3000_regs.h                # 暫存器位址
┃  ┣ 📝 dw3000_vals.h                # 常數與緩衝區偏移
┃  ┣ 📝 dw3000_shared_defines.h      # 實體層常數
┃  ┣ 📝 dw3000_mutex.cpp             # 互斥鎖
┃  ┣ 📝 dw3000_port.h                # Arduino SPI 腳位設定
┃  ┃ 
┃  ┣ 📝 dw3000_config_options.h      # PHY 設定索引表
┃  ┣ 📝 dw3000_config_options.cpp    # 設定結構體實例
┃  ┃ 
┃  ┣ 📝 dw3000_device_api.h          # 暫存器讀寫, 修改巨集
┃  ┣ 📝 dw3000_device_api.cpp        # 晶片底層 API
┃  ┃     
┃  ┣ 📝 dw3000_mac_802_15_4.h        # MAC 訊框與安全標頭定義
┃  ┣ 📝 dw3000_mac_802_15_4.cpp      # MAC 與安全層處理
┃  ┃ 
┃  ┣ 📝 dw3000_shared_functions.h    # 驗證工具函式宣告
┃  ┣ 📝 dw3000_shared_functions.cpp  # 資料包指標工具
┃  ┃ 
┃  ┣ 📝 dw3000_uart.h                # UART 鮑率設定
┃  ┗ 📝 dw3000_uart.cpp              # 序列埠通訊
┃
┣ 📂 Draw_Error_Images  # 統計圖表
┣ 📂 USL2               # 雜項程式
┣ 
┣ 📂 Anchor_Encryption
┃  ┗ 📟 Anchor_Encryption.ino  # Anchor 程式 (接收)
┣ 📂 Tag_Encryption
┃  ┗ 📟 Tag_Encryption.ino     # Tag 程式 (發射)
┣ 
┣ 🐍 2D_position_display.py    # 2D 定位顯示
┣ 🐍 Draw_dis_ns.py            # 距離/延遲圖
┃
┣ 🐍 Draw_res_jitter_ns.py  # 多 Tag 殘差/跳動/延遲圖
┣ 🐍 Positioning.py         # 場域佈置圖
┃
┣ 🐍 Draw_packet.py         # 封包格式圖
┣ 🐍 UDP_to_Wireshark.py    # 封包側錄
┃
┣ 📝 README.md         # 英文說明文件
┣ 📝 README.zh-TW.md   # 中文說明文件
┣ 📋 requirements.txt  # 所有使用的 python 插件
┗ 📝 LICENSE
```

---

## ⚙️ 前置安裝設定

### 1. 硬體部分

安裝 USB 驅動程式：https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads

> 根據電腦環境不同，可分為下列兩種作業軟體安裝 <br>
> (Windows) `CP210x Universal Windows Driver` <br>
> (Mac) `CP210x VCP Mac OSX Driver` <br>
> 安裝後 Arduino 就能正確偵測各個板子

---

### 2. Arduino 部分 
需要把 `DW3000資料夾`，放入到 `libraries資料夾` 裡面。
```bash
 .\Arduino\libraries 
```
Arduino 內部設定為：
```bash
 上方工具欄 -> tools 
```
| 設定項目 | 設定值 |
| :--- | :--- |
| `Board` | ESP32 Dev Module |
| `Port` | 取決於你的 USB 孔位 |
| `CPU Frequency` | 240MHz (WiFi/BT) |
| `Core Debug Level` | None |
| `Erase All Flash Before Sketch Upload` | Disabled |
| `Events Run On` | Core 1 |
| `Flash Frequency` | 80MHz |
| `Flash Mode` | QIO |
| `Flash Size` | 4MB (32Mb) |
| `JTAG Adapter` | Disabled |
| `Arduino Runs On` | Core 1 |
| `Partition Scheme` | Default 4MB with spiffs (1.2MB APP/1.5MB SPIFFS) |
| `PSRAM` | Disabled |
| `Upload Speed` | 921600 |

> 注意：如果程式編譯後出現以下情況：
> ```cpp
> sketch_name.ino:X:XX: fatal error: XXX.h: No such file or directory
> #include <XXX.h>
>          ^~~~~~~
> compilation terminated.
> exit status 1
> Compilation error: XXX.h: No such file or directory
> ```
> 請自行在 Arduino 內部安裝該插件，或是在網路上查詢相關插件並丟入libraries資料夾。

---

### 3. Python 部分 
在 VSCode 的終端機中，安裝 Python 程式所需要的插件
```bash
pip install -r requirements.txt
```
| 插件名稱 | 版本 | 用途 |
| :--- | :--- | :--- |
| `numpy` | `2.2.6` | 負責高效陣列與矩陣運算
| `pandas` | `2.3.1` | 負責表格數據分析與整理
| `matplotlib` | `3.10.5` | 負責繪製基礎圖表
| `seaborn` | `0.13.2` | 負責繪製美觀、進階的統計圖表
| `pyserial` | `3.5` | 負責電腦與 ESP32 的 USB 序列埠通訊

> 注意：如果程式執行後出現以下情況：
> ```py
> Traceback (most recent call last):
>   File "XX.py", line X, in <module>
>     import XXX
> ModuleNotFoundError: No module named 'XXX'
> ```
> 請自行在 VScode 內部安裝 `pip install 該插件`，或是在網路上查詢如何安裝該插件。

---

## 📁 程式碼

### Tag_Encryption.ino

> **角色**：主動發送 Poll 封包、接收 Anchor 回覆、計算飛行時間（ToF）與距離，並透過序列埠或 WiFi UDP 廣播結果。

#### 環境設定

```cpp
// 系統中總共有幾個 Tag 在輪流測距（1 ~ 4）
int totalTags = 4;

// 場域中部署的 Anchor 總數（1 ~ 4）
#define NUM_ANCHORS 4
```

| 參數 | 說明 |
| :--- | :--- |
| `totalTags` | 多 Tag 分時輪詢時須填入總數，分配時段給各個 Tag 去傳收封包 |
| `NUM_ANCHORS` | 設定 Tag 依序向哪些 Anchor 發起測距；此值會影響 `ANCHOR_LIST` 的展開數量 |

#### 加密設定

```cpp
// Tag 識別名稱（T1 ~ T4）
const uint8_t TAG_ADDR[] = { 'T', '1' };

// 啟用 STS 加密
#define STS_ENCRYPTION   false  // false | true

// 啟用 AES-CCM 加密
#define AES_ENCRYPTION   false  // false | true

// 填充位元組（0 ~ 47）
#define Padding  0

// 隨機 Nonce 字節數（0 ~ 4）
#define Random_Nonce_Byte  0
```

| 參數 | 預設值 | 說明 |
| :--- | :---: | :--- |
| `TAG_ADDR` | `'T','1'` | 2 字元識別碼，同時作為網路層短地址。建議依序命名 T1 ~ 。 |
| `STS_ENCRYPTION` | `false` | 開啟後啟用 DW3000 硬體 STS 功能，對 PHR 進行加解密，防止實體層竄改 |
| `AES_ENCRYPTION` | `false` | 開啟後對 MAC Payload 進行 AES-CCM 加密，確保資料機密性 |
| `Padding` | `0` | 在封包末端填入特定長度的無意義位元組，用於壓力測試或模擬不同封包尺寸 |
| `Random_Nonce_Byte` | `0` | 指定 `初始向量 Nonce` 的隨機位元組數，數值越大碰撞機率越低但搜尋時間越長 |

> **加密組合建議**：
> - `STS=false, AES=false`：純測距模式，延遲最低
> - `STS=true, AES=false`：僅實體層保護，適用於對距離精度要求高的場景
> - `STS=false, AES=true`：僅 MAC Payload 加密，適用於需保護測距結果的場景
> - `STS=true, AES=true`：雙重保護（目前在測試階段，不建議正式使用）

#### 網路設定

```cpp
// WiFi 連線資訊
#define tmp_ssid      "SSID"
#define tmp_password  "PASSWORD"
```

#### 多標籤設定

```cpp
// 每個 Tag 分配的時間槽長度（ms）
unsigned long slotDuration = 30;

// 啟用分時機制（當 totalTags > 1 時必須設為 true）
#define window_mode true
```

| 參數 | 說明 |
| :--- | :--- |
| `slotDuration` | 每個 Tag 專屬的傳輸窗口。窗口內 Tag 會依序向所有 Anchor 發起測距 |
| `window_mode` | `true` 啟用分時多工，避免多 Tag 同時發送造成碰撞<br>`false` 持續不斷測距，屬於單 Tag 專用 |

> 系統時間被切割成 `totalTags × slotDuration` 的循環週期。每個 Tag 只在自己的 `(myTagID-1) × slotDuration ∼ myTagID × slotDuration` 時間窗口內發送，其餘時間保持閒置狀態。

---

### Anchor_Encryption.ino

> **角色**：被動監聽 Poll 封包、記錄到達時間、回傳 Response（內含雙方時戳）。Anchor 不計算距離，僅負責協助 Tag 完成雙向測距。

#### 加密與安全設定

```cpp
// Anchor 識別名稱（A1 ~ A4）
const uint8_t ANCHOR_ADDR[] = { 'A', '1' };

// STS 加密（需與 Tag 端一致）
#define STS_ENCRYPTION  false  // false | true

// AES 加密（需與 Tag 端一致）
#define AES_ENCRYPTION  false  // false | true

// 額外填充位元組（需與 Tag 端一致）
#define Padding  0
```

| 參數 | 預設值 | 說明 |
| :--- | :---: | :--- |
| `ANCHOR_ADDR` | `'A','1'` |2 字元識別碼。建議依序命名 A1 ~ 。 |
| `STS_ENCRYPTION` | `false` | 需與所有 Tag 使用相同設定，否則 STS 金鑰比對失敗會導致封包被丟棄 |
| `AES_ENCRYPTION` | `false` | 需與所有 Tag 使用相同設定，否則解密失敗 |
| `Padding` | `0` | 必須與 Tag 端的 `Padding` 值一致，否則封包長度不匹配會造成解析錯誤 |

---

## 🐍 Python 測距程式

### 2D_position_display.py

> 透過 `UDP 通訊協定` 接收 Tag 的 `JSON 測距資料`，在二維平面圖上即時呈現 Tag 位置，支援 3 Anchor 三角定位。

#### 網路設定
```python
# 綁定 UDP 接收 IP（須與 Tag WiFi 處於同一網段）
sock.bind(('192.168.0.108', 8001))

# 實體 Anchor 間距（公尺）
self.distance_A1_A2 = 2.0
```

**`功能特色`**
- **多 Anchor 連線視覺化**：藍色線段連接各 Anchor 形成定位場域
- **距離圈顯示**：以 Anchor 為圓心繪製測距半徑圓（可切換顯示）
- **EKF 卡爾曼濾波器**：內建擴展卡爾曼濾波器，平滑軌跡並降低噪點
- **原始點 vs 濾波點**：同時顯示原始測量點與 EKF 預測點
- **歷史軌跡**：顯示最近 40 筆位置的移動軌跡
- **速度計算**：根據 EKF 狀態向量自動估算即時移動速度


**`按鈕功能`**
| 按鈕 | 功能 |
| :--- | :--- |
| `Raw` | 切換原始測量點的顯示 |
| `Circles` | 切換 Anchor 距離圈的顯示 |
| `EKF` | 切換卡爾曼濾波預測點與軌跡的顯示 |

---


### Draw_dis_ns.py 

> 透過序列埠，即時接收測距資料並繪製 `距離 Distance` 與 `延遲 Latency` 圖。

#### 自訂設定
```python
PORT = 'COM10'             # 序列埠編號（取決於你的 USB 孔位）
BAUD_RATE = 115200         # 鮑率
DATA_LIMIT = 5000          # 單次擷取的資料筆數上限
padding = '0'              # 當前測試的 Padding 值（用於檔案命名與統計分類）
encryption = 'AES_'        # 加密模式前綴（non- / STS_ / AES_ / AES+STS_）
```

**`功能特色`**
- 雙圖並排顯示：左圖為距離（m），右圖為延遲（ns）
- 自動計算並標示平均值（紅色虛線）與標準差
- 支援資料自動存檔（JSON 格式），累積多輪測試結果

> 執行程式後，從序列埠讀取資料。採集達 `DATA_LIMIT` 筆後自動儲存圖表至 `Draw_Error_Images/` 資料夾。

---

## 🐍 Python 封包程式

### Draw_packet.py

> 輸入 Hex 格式的 UWB 封包，自動解析其結構並繪製`封包格式圖`，支援 DW1000 與 DW3000 兩種晶片的協議格式。

**支援的封包類型（DW3000）**：
| 封包類型 | 識別條件 | 說明 |
| :--- | :--- | :--- |
| `Poll` | 第 10 個字節 = 0xE0 | Tag 發送的測距請求 |
| `Response` | 第 10 個字節 = 0xE1 | Anchor 回覆的測距回應（內含時戳） |
| `Poll AES` | FCF = 0x09, 0xEC | 啟用 AES 加密後的 Poll 封包（含安全標頭） |

**使用方式**：
```bash
python Draw_packet.py
# 接著在終端機貼上 Hex 封包字串即可
```

---

### UDP_to_Wireshark.py

> 偵聽 UDP 廣播封包，將測距資料轉為標準格式輸出，需要搭配 Wireshark 進行封包分析。

---

## License

Apache License 2.0. See `LICENSE`.