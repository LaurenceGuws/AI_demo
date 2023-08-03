import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-options',
  templateUrl: './options.component.html',
  styleUrls: ['./options.component.css']
})
export class OptionsComponent implements OnInit {
  models = [];
  selectedModel = '';
  showDropdown = false;

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.getModels();
  }

  toggleDropdown(): void {
    this.showDropdown = !this.showDropdown;
  }

  getModels(): void {
    this.http.get('http://localhost:30000/get_models').subscribe(
      (data: any) => {
        this.models = data;
        this.selectedModel = data[0];
      },
      error => {
        console.error('Error:', error);
      }
    );
  }

  changeModel(): void {
    this.http.post('http://localhost:30000/change_model', { model_name: this.selectedModel }).subscribe(
      (data: any) => {
        // Here you could emit an event to tell the ChatComponent to refresh the messages
      },
      error => {
        console.error('Error:', error);
      }
    );
  }

  uploadFile(event: any): void {  // Add this method
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    this.http.post('http://localhost:30000/upload', formData).subscribe(
      (data: any) => {
        console.log(data);
      },
      error => {
        console.error('Error:', error);
      }
    );
  }

  startNewConversation(): void {
    // Your code to start a new conversation goes here
  }

  customInstructions(): void {
    // Logic for custom instructions will go here
  }

  newChat(): void {
    // Logic for starting a new chat will go here
  }
}
