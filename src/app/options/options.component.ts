import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ChatService } from '../chat.service';

@Component({
  selector: 'app-options',
  templateUrl: './options.component.html',
  styleUrls: ['./options.component.css']
})
export class OptionsComponent implements OnInit {
  models = [];
  selectedModel = '';
  showDropdown = false;
  showCustomInstructionsPopup = false;  // New property
  exampleRequest = '';  // New property
  exampleResponse = '';  // New property

  constructor(private http: HttpClient, private chatService: ChatService) { }

  ngOnInit(): void {
    this.getModels();
  }

  toggleDropdown(): void {
    this.showDropdown = !this.showDropdown;
  }

  toggleCustomInstructionsPopup(): void {  // New method
    this.showCustomInstructionsPopup = !this.showCustomInstructionsPopup;
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

  customInstructions(): void {
    this.http.post('http://localhost:30000/custom_instructions', 
                   {example_request: this.exampleRequest, example_response: this.exampleResponse}).subscribe(
      (data: any) => {
        console.log(data);
      },
      error => {
        console.error('Error:', error);
      }
    );
  }

  newChat(): void {
    this.http.post('http://localhost:30000/new_conversation', {}).subscribe(
      (data: any) => {
        // Clear the chat messages and start a new conversation
        this.chatService.clearMessages();
      },
      error => {
        console.error('Error:', error);
      }
    );
  }

  submitCustomInstructions(): void {
    const instructions = {
      example_request: this.exampleRequest,
      example_response: this.exampleResponse
    };

    this.http.post('http://localhost:30000/custom_instructions', instructions).subscribe(
      (data: any) => {
        console.log(data);
        this.showCustomInstructionsPopup = false; // Close the custom instructions popup
        this.showDropdown = false; // Close the options dropdown
      },
      error => {
        console.error('Error:', error);
      }
    );
  }
}
