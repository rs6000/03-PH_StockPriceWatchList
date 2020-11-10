# 用 Python + Tkinter 做一個看盤小工具 (打包成EXE檔)   

### 前言:
這是一個 菲律賓股票的看盤小程式，因為本人找不到一個可以在
PC上面使用的菲股看盤工具，所以就邊學(Python Tkinter GUI)邊做
想提供給同樣有在關注菲律賓股票的同好們。下載執行檔 [(請按這邊)](https://mega.nz/file/vt4RlYYI#D0l07YPed7PJekpwjPPC8nISATix3Z1bJxPJvIZgi6s)

這隻程式碼只有200多行，原始碼可以在這邊查閱，也提供已經打包好的可執行檔(for Win10)另外也可以照著以下的說明，自行把原始碼打包成可執行檔(for Win10)如果有資安疑慮的...請跳過這篇...
>本篇內容需要以下的材料:  
>> * Python 3.7.2  32bit [(按此下載)](https://www.python.org/downloads/release/python-372/)
>> * 安裝pyhton 虛擬環境 (推薦使用 virtualenvwrapper-win)
>> * Git (如果直接下載本程式zip檔，可以省略)
 ### 快速懶人包:  
直接使用本篇的範例程式:  
    $ git clone https://github.com/rs6000/03-PH_StockPriceWatchList.git
    $ cd myapp (資料夾自己命名)
    $ pip install virtualenvwrapper-win
    $ mkvirtualenv tk (tk可以自己命名)
    $ workon tk
    $ pip install -r requirements.txt 
    $ pyinstaller -F -w PH_StockWatchList.py
以上執行到最後一個步驟，就會執行打包(轉成EXE)的工作，大約幾分鐘後
就會產生一個 build的資料夾，可執行檔(.EXE)就在裡面，打完收工。

### 最後:  
如果程式運行有什麼Bug，請在這邊回報issues

---  
### Reference:  
- [# Python Tkinter GUI Tutorial: To Do List 1](https://www.youtube.com/watch?v=OAHLwtmdqUk) 從這隻範例檔開始學Tkinter
