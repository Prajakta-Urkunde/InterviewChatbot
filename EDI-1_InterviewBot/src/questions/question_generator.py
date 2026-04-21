import random
import json
import os
from typing import List, Dict

class QuestionGenerator:
    def __init__(self):
        self.branches = {
            "cs": "Computer Science",
            "ece": "Electronics and Communication",
            "eee": "Electrical and Electronics",
            "mech": "Mechanical Engineering",
            "civil": "Civil Engineering",
            "chemical": "Chemical Engineering",
            "biotech": "Biotechnology",
            "mba": "Business Administration",
            "medical": "Medical Sciences"
        }
        
        # Load questions from JSON file if available, else use built-in
        self.question_bank = self.load_question_bank()
        
    def load_question_bank(self):
        """Load questions from JSON file or use default if not available"""
        json_path = "data/questions.json"
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r') as f:
                    return json.load(f)
            except:
                return self.get_default_questions()
        else:
            return self.get_default_questions()
    
    def get_default_questions(self):
        """Return a comprehensive set of questions for various branches"""
        return {
            "cs": [
                {
                    "question": "What is object-oriented programming and what are its main principles?",
                    "ideal_answer": "Object-oriented programming (OOP) is a programming paradigm based on the concept of objects. Its main principles are encapsulation, inheritance, polymorphism, and abstraction. Encapsulation bundles data and methods, inheritance allows classes to inherit properties, polymorphism enables different implementations, and abstraction hides complex implementation details."
                },
                {
                    "question": "Explain the difference between TCP and UDP protocols.",
                    "ideal_answer": "TCP (Transmission Control Protocol) is connection-oriented, reliable, and ensures ordered delivery of data with error checking. UDP (User Datagram Protocol) is connectionless, unreliable, and faster but doesn't guarantee delivery or order. TCP is used for applications requiring reliability like web browsing, while UDP is used for real-time applications like video streaming."
                },
                {
                    "question": "What is a binary search tree and what are its properties?",
                    "ideal_answer": "A binary search tree (BST) is a node-based binary tree data structure with the following properties: 1) The left subtree of a node contains only nodes with keys lesser than the node's key. 2) The right subtree of a node contains only nodes with keys greater than the node's key. 3) The left and right subtree each must also be a binary search tree. This structure allows efficient searching, insertion, and deletion operations."
                },
                {
                    "question": "What is the difference between SQL and NoSQL databases?",
                    "ideal_answer": "SQL databases are relational, table-based databases with predefined schema. They use SQL for querying and are vertically scalable. NoSQL databases are non-relational, document, key-value, graph, or wide-column stores. They have dynamic schema, are horizontally scalable, and are better for unstructured data. SQL databases provide ACID compliance while NoSQL follows CAP theorem."
                },
                {
                    "question": "Explain the concept of machine learning and its main types.",
                    "ideal_answer": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. The main types are: 1) Supervised learning (trained on labeled data), 2) Unsupervised learning (finds patterns in unlabeled data), 3) Reinforcement learning (learns through rewards and punishments), and 4) Semi-supervised learning (uses both labeled and unlabeled data)."
                },
                {
                    "question": "What is cloud computing and what are its service models?",
                    "ideal_answer": "Cloud computing is the delivery of computing services over the internet. Its main service models are: 1) Infrastructure as a Service (IaaS) - provides virtualized computing resources, 2) Platform as a Service (PaaS) - provides platforms for developing and deploying applications, and 3) Software as a Service (SaaS) - provides software applications over the internet. Additional models include Function as a Service (FaaS) and Database as a Service (DBaaS)."
                },
                {
                    "question": "Explain the OSI model and its layers.",
                    "ideal_answer": "The OSI (Open Systems Interconnection) model is a conceptual framework that divides network communications into seven layers: 1) Physical (transmission of raw bits), 2) Data Link (error detection/correction), 3) Network (routing), 4) Transport (end-to-end connections), 5) Session (manages connections), 6) Presentation (data translation/encryption), and 7) Application (network services to applications). Each layer serves the layer above it and is served by the layer below it."
                },
                {
                    "question": "What is the difference between process and thread?",
                    "ideal_answer": "A process is an independent program in execution with its own memory space, while a thread is a lightweight process that shares memory space with other threads in the same process. Processes are isolated from each other, whereas threads can easily communicate with each other. Creating a process is more resource-intensive than creating a thread. Multiple threads can exist within a single process."
                },
                {
                    "question": "What are design patterns and name some common ones.",
                    "ideal_answer": "Design patterns are reusable solutions to common software design problems. Common patterns include: 1) Creational patterns (Singleton, Factory, Builder), 2) Structural patterns (Adapter, Decorator, Facade), and 3) Behavioral patterns (Observer, Strategy, Command). Patterns help create more maintainable, flexible, and understandable code by providing proven development paradigms."
                },
                {
                    "question": "Explain the concept of Big O notation and its importance.",
                    "ideal_answer": "Big O notation describes the performance or complexity of an algorithm by expressing how the runtime or space requirements grow as the input size grows. It's important because it helps compare algorithm efficiency independent of hardware. Common complexities include O(1) constant time, O(log n) logarithmic, O(n) linear, O(n²) quadratic, and O(2ⁿ) exponential. It helps developers choose the most efficient algorithm for their needs."
                }
            ],
            "ece": [
                {
                    "question": "What is the difference between analog and digital signals?",
                    "ideal_answer": "Analog signals are continuous waves that change over time, representing physical measurements. Digital signals are discrete, non-continuous signals represented by binary values (0s and 1s). Analog signals are susceptible to noise and degradation, while digital signals can be cleaned and regenerated. Most modern electronics process digital signals for better accuracy and noise immunity."
                },
                {
                    "question": "Explain the working principle of a transistor.",
                    "ideal_answer": "A transistor is a semiconductor device used to amplify or switch electronic signals. It consists of three layers of semiconductor material (emitter, base, and collector). In a bipolar junction transistor (BJT), a small current at the base controls a larger current between the collector and emitter. In field-effect transistors (FET), voltage at the gate controls current between source and drain. Transistors form the building blocks of modern electronic devices."
                },
                {
                    "question": "What is modulation and why is it important in communication systems?",
                    "ideal_answer": "Modulation is the process of varying one or more properties of a high-frequency carrier wave in proportion to a modulating signal. It's important because: 1) It allows efficient radiation of signals through antennas, 2) Enables multiplexing of multiple signals, 3) Reduces antenna size requirements, 4) Improves signal-to-noise ratio, and 5) Allows frequency assignment to avoid interference. Common modulation techniques include AM, FM, and PM."
                },
                # Add more ECE questions as needed
            ],
            "eee": [
                {
                    "question": "Explain Kirchhoff's current and voltage laws.",
                    "ideal_answer": "Kirchhoff's Current Law (KCL) states that the algebraic sum of currents entering and leaving a node is zero. Kirchhoff's Voltage Law (KVL) states that the algebraic sum of all voltages around any closed loop in a circuit is zero. These laws are fundamental for circuit analysis and are based on the conservation of charge and energy principles respectively."
                },
                {
                    "question": "What is the difference between AC and DC power?",
                    "ideal_answer": "AC (Alternating Current) periodically reverses direction and changes magnitude continuously. DC (Direct Current) flows in one direction with constant magnitude. AC is used for power transmission over long distances due to easier voltage transformation and lower losses. DC is used in electronic devices, batteries, and applications requiring constant voltage. Most household appliances convert AC to DC for operation."
                },
                # Add more EEE questions as needed
            ],
            "mech": [
                {
                    "question": "Explain the laws of thermodynamics.",
                    "ideal_answer": "The four laws of thermodynamics are: 1) Zeroth Law: If two systems are in thermal equilibrium with a third, they are in equilibrium with each other. 2) First Law: Energy cannot be created or destroyed, only converted (conservation of energy). 3) Second Law: Entropy of an isolated system never decreases. 4) Third Law: As temperature approaches absolute zero, entropy approaches a minimum constant value."
                },
                # Add more Mechanical questions as needed
            ],
            # Add questions for other branches
        }
    
    def get_available_branches(self):
        """Return available branches with their full names"""
        return self.branches
    
    def get_branch_name(self, branch_code):
        """Get full branch name from code"""
        return self.branches.get(branch_code, branch_code.upper())
    
    def get_questions(self, branch, num_questions=5):
        """Get questions for a specific branch"""
        branch = branch.lower()
        
        if branch in self.question_bank:
            questions = self.question_bank[branch]
            # Return random questions, but not more than available
            return random.sample(questions, min(num_questions, len(questions)))
        else:
            # Fallback for unknown branches
            return [
                {
                    "question": f"Tell me what you know about {self.get_branch_name(branch)}",
                    "ideal_answer": f"{self.get_branch_name(branch)} is a field that involves specialized knowledge. A good answer would demonstrate understanding of key concepts, applications, and possibly recent developments in the field."
                },
                {
                    "question": f"What are the main concepts in {self.get_branch_name(branch)}?",
                    "ideal_answer": f"The main concepts in {self.get_branch_name(branch)} typically include fundamental principles, key methodologies, and important applications. A comprehensive answer would cover these aspects with specific examples."
                }
            ]
    
    def add_questions_from_file(self, file_path):
        """Add questions from an external JSON file"""
        try:
            with open(file_path, 'r') as f:
                new_questions = json.load(f)
            
            # Merge with existing questions
            for branch, questions in new_questions.items():
                if branch in self.question_bank:
                    self.question_bank[branch].extend(questions)
                else:
                    self.question_bank[branch] = questions
            
            # Save the updated question bank
            self.save_question_bank()
            return True
        except Exception as e:
            print(f"Error loading questions from file: {e}")
            return False
    
    def save_question_bank(self):
        """Save the question bank to a JSON file"""
        os.makedirs("data", exist_ok=True)
        with open("data/questions.json", 'w') as f:
            json.dump(self.question_bank, f, indent=2)
            