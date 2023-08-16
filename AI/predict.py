import torch
import torch.nn as nn


# Define the model
class NextNumberPredictor(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(NextNumberPredictor, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x, _ = self.lstm(x)
        x = self.fc(x)
        return x

    # Train the model
    def train(model, data, loss_fn, optimizer, num_epochs):
        for epoch in range(num_epochs):
            for input_sequence, target in data:
                input_sequence = torch.Tensor(input_sequence).view(len(input_sequence), 1, -1)
                target = torch.Tensor(target).view(len(target), -1)

                # Forward pass
                output = model(input_sequence)
                loss = loss_fn(output, target)

                # Backward pass
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

    # Test the model
    def test(model, data, loss_fn):
        total_loss = 0
        for input_sequence, target in data:
            input_sequence = torch.Tensor(input_sequence).view(len(input_sequence), 1, -1)
            target = torch.Tensor(target).view(len(target), -1)
            output = model(input_sequence)
            total_loss += loss_fn(output, target).item()
        return total_loss / len(data)


# Setup the model, data, loss function and optimizer
model = NextNumberPredictor(1, 32, 1)
data = [(list(range(10)), list(range(1, 11))), (list(range(10, 20)), list(range(11, 21)))]
loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters())

# Train the model
NextNumberPredictor.train(model, data, loss_fn, optimizer, num_epochs=100)

# Use the model to make predictions
input_sequence = torch.Tensor(list(range(10, 20))).view(10, 1, -1)
output = model(input_sequence)
prediction = output[-1].item()
print(f'Predicted next number: {prediction:.4f}')