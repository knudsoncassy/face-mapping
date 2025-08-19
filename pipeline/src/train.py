import torch
from torch.utils.data import DataLoader, TensorDataset
from model import LandmarkMLP
from load_data import load_dataset

def train_model(csv_path, epochs=50, batch_size=32, lr=1e-3):
    X, Y, _ = load_dataset(csv_path)
    dataset = TensorDataset(X, Y)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = LandmarkMLP().cuda()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = torch.nn.MSELoss()

    for epoch in range(epochs):
        total_loss = 0
        for xb, yb in loader:
            xb, yb = xb.cuda(), yb.cuda()
            pred = model(xb)
            loss = loss_fn(pred, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}: Loss = {total_loss:.4f}")

    torch.save(model.state_dict(), "landmark_model.pt")
4️⃣ evaluat