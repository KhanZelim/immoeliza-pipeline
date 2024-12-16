from .removing_missing_val import Missing_value_remover
from .removing_outliers import Outlier_remover
from .encoding_categorical import Categorical_encoder
from .training_models import Models_trainer



class Creator:
    def __init__(self) -> None:
        self.mv_remover = Missing_value_remover()
        self.outlier_remover = Outlier_remover()
        self.encoder = Categorical_encoder()
        self.trainer = None

    def preproceed_data(self):
        self.mv_remover.remov_all_missing_values()
        self.outlier_remover.remove_all_outliers()
        self.encoder.encode_df()
    
    def create_models(self):
        self.preproceed_data()
        self.trainer = Models_trainer()
        self.trainer.saving_LinearRegressionModel()
        self.trainer.saving_XGBmodel()
