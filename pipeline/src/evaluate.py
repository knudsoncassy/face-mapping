import torch
import matplotlib.pyplot as plt
from model import LandmarkMLP
from load_data import load_dataset

def evaluate(csv_path):
    X, Y, _ = load_dataset(csv_path)
    model = LandmarkMLP().cuda()
    model.load_state_dict(torch.load("landmark_model.pt"))
    model.eval()

    with torch.no_grad():
        preds = model(X.cuda()).cpu().numpy()
        targets = Y.numpy()

    mse = ((preds - targets) ** 2).mean()
    print(f"Average MSE: {mse:.4f}")

    # Plot sample frames
    for i in range(0, len(preds), len(preds)//5):  # 5 samples
        plt.figure(figsize=(4, 4))
        pred_pts = preds[i].reshape(9, 2)
        true_pts = targets[i].reshape(9, 2)
        plt.scatter(true_pts[:, 0], true_pts[:, 1], c='red', label='Actual')
        plt.scatter(pred_pts[:, 0], pred_pts[:, 1], c='blue', label='Predicted')
        plt.legend()
        plt.title(f"Frame {i}")
        plt.savefig(f"frame_{i}_comparison.png")
        plt.close()