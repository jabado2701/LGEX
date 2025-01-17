# Explanation of the Steps in the Workflow

This workflow tests a project that combines multiple AWS services such as Lambda, S3, and SQS, along with other tools like LocalStack and Terraform. It also validates the functionality of Python scripts and APIs that interact with these services. Each step plays a vital role in ensuring the system operates correctly in a local testing environment.

---

### **1. Clone the Repository Code**
The workflow begins by cloning the repository using the GitHub `actions/checkout` action. This ensures the latest version of the project code is available for testing and deployment.

---

### **2. Set AWS Credentials for LocalStack**
AWS credentials are configured locally to interact with LocalStack. Dummy credentials (`test`) are used to create `.aws/credentials` and `.aws/config` files. These configurations allow seamless access to LocalStack's emulated AWS services.

---

### **3. Start LocalStack**
A Docker container for LocalStack is started, enabling a local AWS-like environment for testing. It includes services like S3, Lambda, IAM, and SQS. This eliminates the need to use real AWS infrastructure during development and testing.

---

### **4. Wait for LocalStack to Be Ready**
A short delay ensures that LocalStack has enough time to initialize before proceeding to subsequent steps.

---

### **5. Install Terraform**
Terraform is installed to manage the infrastructure. This step prepares the environment for executing Terraform commands, which will create resources like S3 buckets, Lambda functions, and SQS queues in LocalStack.

---

### **6. Install Python Dependencies**
Python libraries, such as `boto3`, `flask`, and `networkx`, are installed to support the execution of scripts and Lambda functions. These dependencies facilitate AWS interactions, API handling, and graph computations.

---

### **7. Initialize Terraform**
The `tflocal` command initializes Terraform with LocalStack as the backend. This prepares Terraform to manage resources in the local testing environment.

---

### **8. Validate Terraform**
Terraform validation ensures that the `.tf` files are correctly structured and ready to deploy the defined infrastructure.

---

### **9. Create a Terraform Plan**
A Terraform plan is generated to preview the changes that will be applied to the infrastructure. This step ensures the changes align with expectations and reduces the risk of deployment errors.

---

### **10. Apply Terraform**
Terraform applies the infrastructure changes, creating the required resources in LocalStack. This includes S3 buckets, Lambda functions, IAM roles, and an SQS queue.

---

### **11. Verify S3 Buckets Creation**
The `lgex-app-bucket` and `lgex-download-bucket` are verified to ensure they were successfully created. This is essential for later steps where these buckets are used to store crawled data and processed graphs.

---

### **12. Verify the SQS Queue Creation**
This step confirms that the `lgex-queue` SQS queue was created successfully. The SQS queue is a critical component for managing events and communication between services.

---

### **13. Verify Lambda Function**
The workflow verifies that the `lgex-batch-processor` Lambda function exists and is ready for execution. This ensures that the function was deployed correctly by Terraform.

---

### **14. Debug PYTHONPATH (Optional)**
The `PYTHONPATH` environment variable is printed for debugging purposes. This confirms that the Python environment is set up correctly for running scripts.

---

### **15. Run the `main_crawler.py` Script**
The `main_crawler.py` script is executed with a timeout to test its functionality. The script interacts with the S3 buckets, downloading data into `lgex-download-bucket` and updating a graph stored in `lgex-app-bucket`.

---

### **16. Verify Books in the Download Bucket**
The contents of the `lgex-download-bucket` are checked to ensure that the `main_crawler.py` script successfully stored the crawled books.

---

### **17. Verify the Graph in the App Bucket**
The contents of the `lgex-app-bucket` are verified to ensure that the graph generated from the crawled books was uploaded correctly.

---

### **18. Verify SQS -> Lambda Event Source Mapping**
This step ensures that the `lgex-queue` SQS queue is properly configured as an event source for the `lgex-batch-processor` Lambda function. It verifies that the queue is ready to trigger the Lambda function when events occur.

---

### **19. Run and Test the API**
The `main_api.py` script is executed to start the API server. The workflow tests the API by:
1. Sending requests (e.g., Dijkstra’s algorithm searches) to the endpoints.
2. Saving the responses in JSON files for inspection.
3. Printing the responses for verification.
4. Finally, stopping the API process to clean up.

A delay is placed between requests to ensure the graph reloads itself properly in order to avoid unnecessary problems.

---
