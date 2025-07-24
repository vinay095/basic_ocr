import json
import requests

def send_receipt_to_ocr_api(image_path):
    url = "https://ocr.asprise.com/api/v1/receipt"
    res = requests.post(url,
        data={
            'api_key': 'TEST',
            'recognizer': 'auto',
            'ref_no': 'oct_python_123'
        },
        files={
            'file': open(image_path, 'rb')
        })

    if res.status_code == 200:
        return json.loads(res.text)
    else:
        raise Exception(f"OCR API failed: {res.status_code} - {res.text}")


def parse_receipt(receipt_json):
    receipt = receipt_json['receipts'][0]
    print(f"Your purchase at {receipt.get('merchant_name', 'Unknown')}")

    for item in receipt.get('items', []):
        print(f"{item['description']} - ${item['amount']}")

    print("-" * 30)
    print(f"Subtotal: {receipt.get('subtotal')}")
    print(f"Tax: {receipt.get('tax')}")
    print("-" * 30)
    print(f"Total: {receipt.get('total')}")


if __name__ == "__main__":
    image_path = "invoice2.jpg"
    result = send_receipt_to_ocr_api(image_path)

    # Save response
    with open("response2.json", "w") as f:
        json.dump(result, f, indent=2)

    # Parse and display
    parse_receipt(result)
