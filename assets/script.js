let ai_right_answer;
let ai_justification;

// Function to request the next question from the server
async function requestNextQuestion(subject_str, difficulty_str) {
    // Send a POST request with the necessary headers and body
    const response = await fetch("/next", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ subject: subject_str, difficulty: difficulty_str })
    });
  
    // If the response is not OK, throw an error.
    if (!response.ok) {
        throw new Error("Fetch error: " + response.status);
    }
  
    // Get the raw text from the response
    const text = await response.text();
    console.log("Raw response text:", text);
  
    // Attempt to parse the raw text into a JSON object
    let data;
    try {
        data = JSON.parse(text);
    } catch (e) {
        console.error("Error parsing JSON the first time:", e);
        throw new Error("Invalid JSON received on first parse");
    }
  
    // If the parsed data is still a string, parse it a second time.
    if (typeof data === "string") {
        try {
            data = JSON.parse(data);
        } catch (e) {
            console.error("Error parsing JSON the second time:", e);
            throw new Error("Invalid JSON received on second parse");
        }
    }
  
    console.debug("Final parsed JSON:", data);
    return data;
  }
  
// Function to update the page with the next question
async function next_question(subject_str, difficulty_str) {
    try {
        // Request the question from the server
        const json = await requestNextQuestion(subject_str, difficulty_str);
    
        // Log the keys of the JSON for debugging
        console.log("Full JSON object:", json);
        console.log("Keys available:", Object.keys(json));
    
        // Verify the response has the 'alternativas' property
        if (!json || !json.hasOwnProperty("alternativas")) {
            throw new Error("The 'alternativas' property is missing in the JSON");
        }
    
        // Get the question and options from the JSON
        const question = json.enunciado || "No question provided";
        const options = json.alternativas;
        const subject = json.resumo;
        ai_right_answer = json.correta;
        ai_justification = json.justificativa;
    
        // Update the DOM with the question text
        document.getElementById("question").innerText = question;
    
        // Ensure the options are an array and update each corresponding DOM element
        if (Array.isArray(options)) {
            options.forEach((option, index) => {
            const el = document.getElementById(`option${index + 1}`);
            if (el) {
                el.innerText = option;
            } else {
                console.warn(`Element with id "option${index + 1}" not found`);
            }
            });
        } else {
            throw new Error("'alternativas' is not an array as expected");
        }
    
        // Update additional fields if their elements exist
        const subjectEl = document.getElementById("subject");
        if (subjectEl) {
            // If 'resumo' is an array, join it into a string
            subjectEl.innerText = Array.isArray(subject) ? subject.join(", ") : subject;
        }
    
        console.log("Question loaded successfully");
    } 

    catch (error) {
        console.error("Failed to load question:", error);
        document.getElementById("content").innerHTML = "<h1>:(</h1><p>Ocorreu um erro na geração da questão. Isso é tudo que sabemos. Tente novamente.</p>";
    }
}

function get_subject_value()
{
    let nodes = document.getElementById("subjects_selector").childNodes;
    for (let i = 0; i < nodes.length; i++) 
    {
        if(nodes[i].checked)
        {
            return nodes[i].value;
        }
    }
    return "any";
}

function get_difficulty_value()
{
    let nodes = document.getElementById("difficulty_selector").childNodes;
    for (let i = 0; i < nodes.length; i++) 
    {
        if(nodes[i].checked)
        {
            return nodes[i].value;
        }
    }
    return "any";
}

async function check_and_request()
{
    document.getElementById("generating").style.display = "block";
    document.getElementById("generating").style.visibility = "visible";
    document.getElementById("selection").style.display = "none";
    document.getElementById("selection").style.visibility = "hidden";

    let subject_str = get_subject_value();
    let difficulty_str = get_difficulty_value();
    
    await next_question(subject_str, difficulty_str);

    document.getElementById("generating").style.display = "none";
    document.getElementById("generating").style.visibility = "hidden";
    document.getElementById("content").style.display = "block";
    document.getElementById("content").style.visibility = "visible";
}

function create_selection()
{
    let parent = document.getElementById("selection");
    parent.innerHTML += "<p>Selecione a matéria</p>";
    parent.innerHTML += "<div class='radio_buttons' id='subjects_selector'>";
    
    let container = document.getElementById("subjects_selector");
    subjects = ["Matemática", "Português", "Inglês", "Espanhol", "Arte", "Educação Física", "Literatura", "Física", "Química", "Biologia", "História", "Geografia", "Filosofia", "Sociologia"];
    for (let i = 0; i < subjects.length; i++) 
    {
        let radio = document.createElement("input");
        radio.type = "radio";
        radio.id = "radio_button_subject_n" + i;
        radio.name = "subjects_selector";
        radio.value = subjects[i];
        container.appendChild(radio);   

        let label = document.createElement("label");
        label.setAttribute("for", "radio_button_subject_n" + i);
        label.innerHTML = subjects[i];
        container.appendChild(label);   
    }

    parent.innerHTML += "</div><br>";
    parent.innerHTML += "<p>Selecione a dificuldade</p>";
    parent.innerHTML += "<div class='radio_buttons' id='difficulty_selector'>";

    container = document.getElementById("difficulty_selector");
    difficulty = ["Fácil", "Média", "Difícil"];
    for (let i = 0; i < difficulty.length; i++) 
    {
        let radio = document.createElement("input");
        radio.type = "radio";
        radio.id = "radio_button_difficulty_n" + i;
        radio.name = "difficulty_selector";
        radio.value = difficulty[i];
        container.appendChild(radio); 
        
        let label = document.createElement("label");
        label.setAttribute("for", "radio_button_difficulty_n" + i);
        label.innerHTML = difficulty[i];
        container.appendChild(label);  
    }

    parent.innerHTML += "</div>";

}

function get_user_answer_value()
{
    let nodes = document.getElementById("content").childNodes;
    for (let i = 0; i < nodes.length; i++) 
    {
        let children = nodes[i].childNodes;
        for (let j = 0; j < children.length; j++) 
        {
            if(children[j].checked)
            {
                return children[j].value;
            }
        }
    }

    return false;
}

function check_answer()
{
    if (get_user_answer_value() == false)
    {
        return;        
    }

    document.getElementById("content").style.display = "none";
    document.getElementById("content").style.visibility = "hidden";

    if (get_user_answer_value() == ai_right_answer.toUpperCase())
    {
        document.getElementById("right_message").style.display = "block";
        document.getElementById("right_message").style.display = "visible";
        document.getElementById("wrong_message").style.display = "none";
        document.getElementById("wrong_message").style.display = "hidden";
    }

    else
    {
        document.getElementById("wrong_message").style.display = "block";
        document.getElementById("wrong_message").style.display = "visible";
        document.getElementById("right_message").style.display = "none";
        document.getElementById("right_message").style.display = "hidden";
    }

    document.getElementById("correct_option_space").innerHTML = ai_right_answer;
    document.getElementById("ai_justification_space").innerHTML = ai_justification;

    document.getElementById("answer_checking").style.display = "block";
    document.getElementById("answer_checking").style.visibility = "visible";
}

function restart()
{
    location.reload();
}
