import joblib
import numpy as np
from skimage.transform import resize

# For predict the blur_digit paramters
scale_reg = joblib.load("./models/scale_setting_reg.joblib")

try:
    model = joblib.load("./models/rf_clf.joblib")
    print("Model found")
except:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import fetch_openml
    
    print("Model not exist, training model...")
    X, y = fetch_openml("mnist_784", return_X_y=True, as_frame=False)

    model = rnc = RandomForestClassifier(n_estimators=116, max_depth=47, random_state=42, n_jobs=-1)
    model.fit(X, y)

    joblib.dump(model, "./models/rf_clf.joblib")
    print("Model trained & saved")

# Reshape the canvas from ([lenght],) to square shape
def reshape_canvas(canvas):
    if len(canvas.shape) == 1:
        size = int(np.sqrt(len(canvas)))
        return canvas.reshape((size, size))
    return canvas

# Add blur and bolds to the canvas, to make it look like the MNIST digits
def blur_digit(canvas, blur=0.8, bold=2):
    dig = reshape_canvas(canvas.copy())
    digit_blured = resize(resize(dig, [round(28 * blur)] * 2, preserve_range=True), (28, 28), preserve_range=True)
    digit_blured = digit_blured * bold
    digit_blured[digit_blured > 255] = 255
    return digit_blured

# Prepare the canvas before to give it to model
def prepare_canvas(canvas, d_size=25):
    canvas = reshape_canvas(canvas)

    # To center the digit
    rows = np.any(canvas, axis=1)
    cols = np.any(canvas, axis=0)
    
    if not rows.any() or not cols.any():
        return canvas.reshape(-1)
    
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    canvas_crop = canvas[max(rmin - 1, 0):rmax + 2, max(cmin - 1, 0):cmax+2]

    # Reshape the canvas, because the canvas that user made is (56, 56), and the model accept (28, 28).
    height, width = canvas_crop.shape
    new_shape = [(d_size if height >= width else round(d_size/width * height)),
                (d_size if width >= height else round(d_size/height * width))]

    canvas_crop = resize(canvas_crop, new_shape, preserve_range=True)
    
    canvas_new = np.zeros((28, 28), dtype=np.int16)

    r_start = (28 - canvas_crop.shape[0]) // 2
    c_start = (28 - canvas_crop.shape[1]) // 2

    # Paste the digit
    canvas_new[r_start:r_start + canvas_crop.shape[0], c_start:c_start + canvas_crop.shape[1]] = canvas_crop

    # Blur & Bold the digit (Make it like MNIST data)
    blur, bold = scale_reg.predict([[height * width]])[0]
    canvas_new = blur_digit(canvas_new, blur, bold)

    return canvas_new.reshape(-1)

def predict(canvas):
    canvas = canvas.reshape(-1)

    try:
        probabs = model.predict_proba([canvas])[0]
        # If the model wasn't confident about prediction, predict "-" (Unknown)
        prediction = probabs.argmax() if probabs.max() > .26 else "-"
        return prediction
    except:
        return "-"