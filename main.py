import datetime
import win32com.client # type: ignore
import os
import pythoncom # type: ignore
import img2pdf

from PIL import Image
from flask import Flask, request # type: ignore

app = Flask(__name__)
devices = []
scan_name = 0
abspath = os.path.abspath("C:/Users/Public/scanned/")
output_path = ""

def compressToSize(image_path, target_kb, outp):
    try:
        tarsize = target_kb * 1024
        fullqual = 95
        print(f"compress to size imagepath: {image_path}")
        img = Image.open(image_path).copy()
        current_size = os.path.getsize(image_path)
        while current_size > tarsize and fullqual > 10:
            img.save(outp, fullqual=fullqual)
            current_size = os.path.getsize(outp)
            fullqual -= 5
        img.close()
        return
    except Exception as e:
        print(f"error during compress: {e}")
        return None
    finally:
        pythoncom.CoUninitialize()

def initscan():
    try:
        pythoncom.CoInitialize()
        wia_dev_man = win32com.client.Dispatch("WIA.DeviceManager")
        devices.clear()
        for i, device_info in enumerate(wia_dev_man.DeviceInfos):
            name = device_info.Properties('Name').Value
            id = device_info.DeviceID
            res = {
                "data": device_info,
                "name": name,
                "ID": id
            }
            devices.append(res)
    finally:
        pythoncom.CoUninitialize()

def initiateScan(fname,resetname,dpix,dpiy,start_x,start_y,h,w,col):
    try:
        global output_path
        pythoncom.CoInitialize()
        initscan()
        global scan_name
        print("Choose Driver: ")
        for i, v in enumerate(devices):
            print(" "+str(i)+". "+v["name"])
        choosen = devices[0]
        print("Choosen Driver: "+choosen["name"])
        choosen_driver = choosen['data'].Connect()

        item = choosen_driver.Items[0]
        item.Properties["6147"].Value = dpix
        item.Properties["6148"].Value = dpiy
        item.Properties["6149"].Value = start_x
        item.Properties["6150"].Value = start_y
        item.Properties["6151"].Value = w
        item.Properties["6152"].Value = h
        item.Properties["6149"].Value = col

        image = item.Transfer()
        if(resetname!=0):
            if(resetname==-1):
                scan_name=0
            else:
                scan_name=resetname
        output_path = f"{abspath}/{fname}{str(scan_name)}.jpg"
        scan_name+=1
        if os.path.exists(output_path):
            os.replace(output_path,output_path)
        else:
            image.saveFile(output_path)

        return request.host
    except Exception as e:
        print(f"error during scan: {e}")
        return None
    finally:
        pythoncom.CoUninitialize()

@app.route('/scan', methods=['GET'])
def main():
    os.makedirs(abspath,exist_ok=True)
    dpi = request.args.get('dpi', default=150, type=int)
    fname = request.args.get('savefname', default='', type=str)
    resetname = request.args.get('reset', default=0, type=int)
    dpi = request.args.get('dpi', default=150, type=int)
    pdf = request.args.get('pdf', default=1, type=int)
    initiateScan(fname,resetname,dpi,dpi,0,0,1754,1240,2)
    # outp_path = f"{abspath}/{fname}{str(scan_name)}.jpg"
    compressToSize(image_path=output_path, target_kb=100, outp=output_path)
    if(pdf==1):
        pdfbyte = img2pdf.convert(output_path)
        with open(f"{output_path.split('.')[0]}.pdf","wb") as f:
            f.write(pdfbyte)
    return "document scanned check shared folder"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)