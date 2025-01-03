import zlib
import base64
class ERD_Util:
    def encode_plantuml(plantuml_code):
        """Encodes PlantUML text to a URL-safe format for the PlantUML server."""
        compressed = zlib.compress(plantuml_code.encode('utf-8'))
        encoded = base64.b64encode(compressed).decode('utf-8')
        return encoded.replace('+', '-').replace('/', '_').replace('=', '')
