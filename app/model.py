from fastai.vision import defaults, torch, load_learner, open_image, BytesIO

class Model:
    def __init__(self, pkl_dir, pkl_file):
        defaults.device = torch.device('cpu')  # run on a CPU
        self.learn = load_learner(path=pkl_dir, file=pkl_file)

    def classify(self, content):
        image = open_image(BytesIO(content))
        pred_class, _pred_idx, _outputs = self.learn.predict(image)
        return str(pred_class)
