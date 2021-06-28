# AUTOGENERATED! DO NOT EDIT! File to edit: 01_model.ipynb (unless otherwise specified).

__all__ = ['MachineLearningModel', 'LogisticRegressionClassifier']

# Cell
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import (
    GridSearchCV,
    cross_val_score,
    train_test_split,
    StratifiedKFold,
)
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler

# Cell
class MachineLearningModel:
    """
    Overly simplified example for a base class: basically just function handle definitions
    """

    def __init__(self, X, y, n_splits=5, seed=0):
        self.n_splits = n_splits  # k-fold n_splits
        self.seed = seed
        self.set_data(X, y)

    def set_data(self, X, y):
        """
        Set traing and evaluation data
        """
        self.X = X.copy()
        self.y = y.copy()

        self.__create_train_test_data()

        return self

    def get_data(self) -> (np.ndarray, np.ndarray):
        """
        Get training and evaluation data
        """
        return self.X.copy(), self.y.copy()

    def __create_train_test_data(self, n_splits=None, seed=None):
        """
        Create training and testing data
        """
        if seed is None:
            seed = self.seed
        if n_splits is None:
            n_splits = self.n_splits

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=(1 / n_splits), random_state=seed, stratify=self.y
        )

        return self

    def get_train_test_data(self):
        """
        Return X_train, X_test, y_train, y_test
        """
        return self.X_train, self.X_test, self.y_train, self.y_test

    def fit(self, X=None, y=None, **fit_params):
        pass

    def predict(self, X):
        pass

    def loss(self, X, y):
        pass

    def get_train_loss(self):
        pass

    def get_test_loss(self):
        pass

    def optimize(self):
        pass

    def get_params(self):
        pass

# Cell
class LogisticRegressionClassifier(MachineLearningModel):
    """
    Logistic regression classifier
    """

    def __init__(self, X, y, n_splits=5, seed=0):

        super(LogisticRegressionClassifier, self).__init__(
            X, y, n_splits=n_splits, seed=seed
        )

        self.scaler = StandardScaler()
        self.model = LogisticRegression()
        self.pipe = Pipeline([("scaler", self.scaler), ("estimator", self.model)])

        # cross validation for optimization
        self.cv = StratifiedKFold(n_splits=self.n_splits)

        # param grid for optimization
        self.param_grid = {
            "estimator__C": np.linspace(0.3, 1.7, 10)  # logspace(-4, 4, 10),
        }

        # define optimization method for optimizing the model
        self.optimization_pipe = GridSearchCV(
            estimator=self.pipe,
            param_grid=self.param_grid,
            scoring="accuracy",
            cv=self.cv,
            return_train_score=True,
        )

    def fit(self, X=None, y=None):
        """
        Train and evaluate model
        """
        if X is None or y is None:
            self.pipe.fit(self.X_train, self.y_train)
        else:  # reset data, recreate training and testing data and recursively call fit
            self.set_data(X, y).fit()

        return self

    def predict(self, X):
        """
        Get predicted value at X
        """
        return self.pipe.predict(X)

    def loss(self, X, y):
        """
        Return loss (model quality metric) [f1 score]

        Note that this may be a different metric than the one that the model optimizer is using (scoring method).
        For example for LogisticRegression the scoring method is mean accuracy,
        but we want to track f1-score for loss because it is better balanced.
        """

        return f1_score(y, self.predict(X))

    def get_train_loss(self):
        """
        Return loss for training data
        """
        return self.loss(self.X_train, self.y_train)

    def get_test_loss(self):
        """
        Return loss for testing data
        """
        return self.loss(self.X_test, self.y_test)

    def optimize(self):
        """
        Optimize model hyperparameters and fit the model with optimized parameters.

        This example is with GridSearchCV, but more efficient algorithms can be implemented in practice.
        """
        self.optimization_pipe.fit(self.X_train, self.y_train)
        self.pipe.set_params(
            estimator__C=self.optimization_pipe.best_params_["estimator__C"]
        )
        self.fit()
        return self

    def get_params(self):
        """
        Return params
        """
        return self.pipe.get_params()