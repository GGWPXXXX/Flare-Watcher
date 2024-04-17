import ubinascii
import uos
import urequests

# Function to create multipart form-data request
def make_request(data, image=None):
    boundary = ubinascii.hexlify(uos.urandom(16)).decode('ascii')

    def encode_field(field_name):
        return (
            b'--%s' % boundary,
            b'Content-Disposition: form-data; name="%s"' % field_name,
            b'', 
            b'%s'% data[field_name]
        )

    def encode_file(field_name):
        filename = 'latest.jpeg'
        return (
            b'--%s' % boundary,
            b'Content-Disposition: form-data; name="%s"; filename="%s"' % (
                field_name, filename),
            b'', 
            image
        )

    lines = []
    for name in data:
        lines.extend(encode_field(name))
    if image:
        lines.extend(encode_file('file'))
    lines.extend((b'--%s--' % boundary, b''))
    body = b'\r\n'.join(lines)

    headers = {
        'content-type': 'multipart/form-data; boundary=' + boundary,
        'content-length': str(len(body))
    }
    return body, headers

# Function to upload image using multipart form-data request
def upload_image(url, headers, data):
    http_response = urequests.post(
        url,
        headers=headers,
        data=data
    )
    if http_response.status_code == 204:
        print('Uploaded request')
    else:
        raise UploadError(http_response)
    http_response.close()
    return http_response

# Define the URL to send the request to
url = 'http://127.0.0.1:8000/predict/image_prediction/'

# Prepare image data
with open("test_img.png", 'rb') as image_file:
    image_data = image_file.read()


