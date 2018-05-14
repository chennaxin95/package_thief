import numpy as np
import alexa

a = alexa.Alexa(0)
img = np.ones((3,24,24)).astype(np.uint8)
a.upload_celery(img)
