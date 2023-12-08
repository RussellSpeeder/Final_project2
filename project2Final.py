import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QStackedWidget
import csv

class VotingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.votes = {}
        self.init_ui()

    def init_ui(self):
        self.step = 0

        layout = QVBoxLayout()

        self.status_label = QLabel("Status: No votes yet")

        self.voter_id_widget = QWidget()
        self.voter_id_layout = QVBoxLayout(self.voter_id_widget)
        self.voter_id_label = QLabel("Enter Voter ID:")
        self.voter_id_input = QLineEdit()
        self.voter_id_layout.addWidget(self.voter_id_label)
        self.voter_id_layout.addWidget(self.voter_id_input)

        self.vote_widget = QWidget()
        self.vote_layout = QVBoxLayout(self.vote_widget)
        self.vote_label = QLabel("Enter the name of the candidate:")
        self.vote_input = QLineEdit()
        self.vote_layout.addWidget(self.vote_label)
        self.vote_layout.addWidget(self.vote_input)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.voter_id_widget)
        self.stacked_widget.addWidget(self.vote_widget)

        submit_button = QPushButton("Submit")
        exit_button = QPushButton("Exit")

        submit_button.clicked.connect(self.submit_action)
        exit_button.clicked.connect(self.close)

        layout.addWidget(self.status_label)
        layout.addWidget(self.stacked_widget)
        layout.addWidget(submit_button)
        layout.addWidget(exit_button)

        self.setLayout(layout)

        self.setWindowTitle("Voting App")
        self.show()

    def submit_action(self):
        if self.step == 0:
            self.submit_voter_id()
        elif self.step == 1:
            self.submit_vote()

    def submit_voter_id(self):
        voter_id = self.voter_id_input.text()

        if not voter_id:
            self.status_label.setText("Status: Please enter Voter ID.")
            return

        if self.check_voter_id(voter_id):
            self.status_label.setText("Status: User already voted")
        else:
            self.votes[voter_id] = ""
            self.voter_id_input.clear()
            self.step = 1
            self.stacked_widget.setCurrentIndex(self.step)
            self.status_label.setText("Status: Voter ID recorded")

    def submit_vote(self):
        vote = self.vote_input.text()

        if not vote:
            self.status_label.setText("Status: Please enter the name of the candidate.")
            return

        voter_id = self.voter_id_input.text()
        self.votes[voter_id] = vote
        self.voter_id_input.clear()
        self.vote_input.clear()
        self.step = 0
        self.stacked_widget.setCurrentIndex(self.step)
        self.status_label.setText("Status: Vote recorded")

        self.save_votes_to_csv()

    def check_voter_id(self, voter_id):
        return voter_id in self.votes

    def save_votes_to_csv(self):
        with open('votes.csv', 'w', newline='') as csvfile:
            fieldnames = ['VoterID', 'Vote']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for voter_id, vote in self.votes.items():
                writer.writerow({'VoterID': voter_id,'Vote': f'{vote}'})

def main():
    app = QApplication(sys.argv)
    window = VotingApp()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()