# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/my_ocr_model.ipynb.

# %% auto 0
__all__ = ['MyYoloOCR']

# %% ../nbs/my_ocr_model.ipynb 2
import torch

# %% ../nbs/my_ocr_model.ipynb 4
class MyYoloOCR:
    """
    Class to load fine tuned model weights to yolov5 and get number plate text
    """

    def __init__(self, weights_file_location="weights/best_150_epochs.pt"):

        self.wfl = weights_file_location

        self.model = torch.hub.load(
            "ultralytics/yolov5", "custom", path=self.wfl, force_reload=True
        )  # yolov5s

        self.class_id_map = self.model.names

    def get_number_plate_text(self, img_path: str, show_result: bool = False) -> str:
        result = self.model(img_path)  # Get result

        if show_result:
            result.show()

        # Get x y h w prob and class id
        result_arr = result.xywhn[0].cpu().numpy().tolist()
        number_bboxs = len(result_arr)
        # print(number_bboxs)

        # Sort result according to x
        result_arr = sorted(result_arr, key=lambda x: x[0])

        # Get class ids and filter out 'EUR'->16 and '-' -> 0
        class_ids = [int(x[-1]) for x in result_arr if int(x[-1]) not in [0, 16]]

        # # Get class ids and filter out 'EUR'->16
        # class_ids = [int(x[-1]) for x in result_arr if int(x[-1]) not in [16]]

        # Get class from ids

        classes = [self.class_id_map[x] for x in class_ids]

        # Make text
        ocr_text = "".join(classes)

        return ocr_text
