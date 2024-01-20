import cv2
import numpy as np
from keras.models import load_model
from OBR import BrailleImage, SegmentationEngine
import string

class PredictBraille:
    def __init__(self):
        self.prediction = ""

    def predict(self, input_image_path):
        print("Let begin")
        alphabet = list(string.ascii_lowercase)
        cur_pos = 0
        target = {}
        for letter in alphabet:
            target[letter] = [0] * 27
            target[letter][cur_pos] = 1
            cur_pos += 1
        target[' '] = [0] * 27
        target[' '][26] = 1

        print("Load model")
        # Load the Braille model
        model = load_model('braille_model_drop.h5')

        # Load the input image
        input_image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
        _, binary_image = cv2.threshold(input_image, 128, 255, cv2.THRESH_BINARY)

        # Save the binary image as a JPEG
        # output_path = 'output.jpg'
        # cv2.imwrite(output_path, binary_image)
        # cv2.imshow("imagee", binary_image)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        # print("Load BImage")
        # Create a BrailleImage instance
        braille_image = BrailleImage(input_image_path)
        # print("load SEngine")
        # Create a SegmentationEngine instance
        segmentation_engine = SegmentationEngine(braille_image)
        prev_word=0
        prev_line=0
        # print("Predict")
        # Loop through segmented characters and predict their classes
        for segmented_character in segmentation_engine:
            character_image = segmented_character.get_character_image()

            box = segmented_character.get_bounding_box()
            left,right,top,bottom = box
            width = int(right - left)
            height =int(bottom-top)

            #word space i.e new word
            if((left-prev_word)>width):
                self.prediction=self.prediction+" "
            prev_word=right
                
            #line space i.e. new line
            if((top-prev_line)>height/4):
                self.prediction=self.prediction+"\n"
            prev_line=bottom

            # Preprocess the character image before passing it to the model
            resized_img = cv2.resize(character_image, (28, 28))
            rgb_character_image = resized_img.reshape(-1, 28, 28, 3)
            pred_img = rgb_character_image.astype(np.float32) / 255.0
            # Perform classification using the loaded model
            pred_lb = model.predict(pred_img)
            pred = ""
            for j in range(len(pred_lb[0])):
                if pred_lb[0][j] > 0.6:
                    pred_lb[0][j] = 1.0
                else:
                    pred_lb[0][j] = 0.0
            for key, value in target.items():
                if np.array_equal(np.asarray(pred_lb[0]), np.asarray(value)):
                    pred = key
            if pred == "":
                pred = "!"
            self.prediction = self.prediction + pred
            # Mark the character's bounding box on the parent image
            segmented_character.mark()
        
        # print(self.prediction)
        # Get the final image with marked bounding boxes
        final_image = braille_image.get_final_image()
        cv2.imshow("image", final_image)
        cv2.waitKey()
        cv2.destroyAllWindows()

        return self.prediction