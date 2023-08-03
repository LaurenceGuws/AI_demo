import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-message-input',
  templateUrl: './message-input.component.html',
  styleUrls: ['./message-input.component.css']
})
export class MessageInputComponent implements OnInit {
  message = '';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  sendMessage(): void {
    if (!this.message) {
      return;
    }

    this.http.post('http://localhost:30000/message', { message: this.message }).subscribe(
      (data: any) => {
        this.message = '';
        // Here you could emit an event to tell the ChatComponent to refresh the messages
      },
      error => {
        console.error('Error:', error);
      }
    );
  }
}
