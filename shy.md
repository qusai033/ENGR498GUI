Here’s a **focused and simplified set of notes** with examples, emphasizing **random variables, CDF, PDF, PMF**, and the other probability topics:

---

### **Probability and Statistics**

#### **1. Conditional Probability**
- Formula: \( P(A|B) = \frac{P(A \cap B)}{P(B)} \).  
- Example (Exam 1): Rolling a die: \( A = \{ \text{even numbers} \}, B = \{ \text{less than 5} \} \).  
  - \( P(A \cap B) = P(\{2, 4\}) = P(2) + P(4) \).  
  - \( P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{\frac{1}{6} + \frac{1}{6}}{\frac{4}{6}} = \frac{1}{2} \).

#### **2. Bayes' Theorem**
- Formula: \( P(A|B) = \frac{P(B|A)P(A)}{P(B)} \).  
- Example (Exam 1): Picking chocolates, compute \( P(F|D) \):  
  - If \( P(D|F) = \frac{8}{13}, P(F) = \frac{1}{2}, P(D) = \frac{6}{13} \), then:  
    \( P(F|D) = \frac{\frac{8}{13} \cdot \frac{1}{2}}{\frac{6}{13}} = \frac{4}{6} = \frac{2}{3} \).

#### **3. Total Probability**
- Formula: \( P(B) = \sum_{i} P(B|A_i)P(A_i) \).  
- Example (Exam 2):  
  Suppose \( A_1 \) and \( A_2 \) are partitions of outcomes (e.g., rolling a 6-sided die).  
  \( P(X = x) = P(X = x | A_1)P(A_1) + P(X = x | A_2)P(A_2) \).

#### **4. Independence**
- Events \( A \) and \( B \) are independent if \( P(A \cap B) = P(A)P(B) \).  
- Example (Exam 1): Rolling a die twice:  
  \( A = \{ \text{First roll odd} \}, B = \{ \text{Second roll odd} \} \).  
  \( P(A \cap B) = \frac{1}{4}, P(A) = \frac{1}{2}, P(B) = \frac{1}{2} \).  
  Since \( P(A \cap B) = P(A)P(B) \), \( A \) and \( B \) are independent.

---

### **Random Variables, CDF, PDF, PMF**

#### **5. Random Variables**
- A function that assigns a numerical value to each outcome of an experiment.  
- **Discrete**: E.g., Number of heads in coin flips.  
- **Continuous**: E.g., Time to complete a task.

#### **6. PMF (Probability Mass Function)**  
- For **discrete** random variables, \( P(X = x) \): Probability of each specific value.  
- Example (Exam 2): Rolling a die, \( X \) is the roll outcome:  
  \( P(X = 1) = \frac{1}{6}, P(X = 2) = \frac{1}{6}, \dots, P(X = 6) = \frac{1}{6} \).

#### **7. PDF (Probability Density Function)**  
- For **continuous** random variables, \( f(x) \): Describes the relative likelihood of a variable at a specific value.  
- \( P(a \leq X \leq b) = \int_a^b f(x) dx \).  
- Example: If \( f(x) = 2x \) for \( 0 \leq x \leq 1 \),  
  \( P(0.2 \leq X \leq 0.5) = \int_{0.2}^{0.5} 2x \, dx \).

#### **8. CDF (Cumulative Distribution Function)**  
- \( F(x) = P(X \leq x) \): Cumulative probability up to \( x \).  
- \( F(x) = \int_{-\infty}^x f(t) dt \) for continuous variables.  
- Example (Exam 2):  
  For PMF \( P(X = 1) = \frac{1}{6}, P(X = 2) = \frac{1}{6}, \dots \):  
  \( F(2) = P(X \leq 2) = P(1) + P(2) = \frac{1}{6} + \frac{1}{6} = \frac{1}{3} \).

#### **9. Binomial Distribution**  
- \( P(X = k) = \binom{n}{k} p^k (1-p)^{n-k} \).  
- Mean: \( \mu = np \), Variance: \( \sigma^2 = np(1-p) \).  
- Example: Flipping a coin \( n = 10 \) times, \( p = 0.5 \), find \( P(X = 6) \):  
  \( P(X = 6) = \binom{10}{6} (0.5)^6 (0.5)^4 = \frac{210}{1024} \).

#### **10. Joint Distributions**  
- Joint PMF (discrete): \( P(X = x, Y = y) \).  
- Example: Rolling two dice, \( P(X = 1, Y = 2) = \frac{1}{36} \).  
- Marginal PMF: \( P(X = x) = \sum_y P(X = x, Y = y) \).  

---

These examples from the uploaded files and foundational formulas should help you during the exam! Let me know if you'd like clarification on any specific concept.
