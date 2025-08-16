from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.depends.get_current_user import get_current_user
from app.core.depends.get_session import get_session
from app.model.model import User
from app.schema.tests import (
    ListeningPassagesResponse,
    ReadingPassagesResponse,
    SpeakingQuestionsResponse,
    WritingPromptsResponse,
)

router = APIRouter(
    prefix="/tests",
    tags=["tests"],
)


@router.get("/speaking/questions", response_model=SpeakingQuestionsResponse)
async def get_speaking_questions(
    difficulty: str = Query(..., description="Difficulty level", enum=["easy", "medium", "hard"]),
    topic: Optional[str] = Query(None, description="Optional topic filter"),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> SpeakingQuestionsResponse:
    """
    Get speaking test questions filtered by difficulty and optionally by topic
    """
    # In a real implementation, this would query the database for questions
    # For now, we'll return mock data

    mock_questions = []

    # Easy questions
    if difficulty == "easy":
        mock_questions = [
            {
                "id": 1,
                "text": "Describe your favorite place to relax. Why do you like it there?",
                "topic": "leisure",
                "difficulty": "easy",
                "category": "personal",
            },
            {
                "id": 2,
                "text": "Talk about a hobby or activity you enjoy. How did you get started with it?",
                "topic": "hobbies",
                "difficulty": "easy",
                "category": "personal",
            },
            {
                "id": 3,
                "text": "Describe your hometown and what you like about it.",
                "topic": "places",
                "difficulty": "easy",
                "category": "personal",
            },
        ]
    # Medium questions
    elif difficulty == "medium":
        mock_questions = [
            {
                "id": 4,
                "text": "Do you think technology has improved how we communicate? Give reasons for your answer.",
                "topic": "technology",
                "difficulty": "medium",
                "category": "opinion",
            },
            {
                "id": 5,
                "text": "Describe a challenge you've faced and how you overcame it.",
                "topic": "challenges",
                "difficulty": "medium",
                "category": "experience",
            },
            {
                "id": 6,
                "text": "How has education changed in the last twenty years? Do you think these changes are positive?",
                "topic": "education",
                "difficulty": "medium",
                "category": "opinion",
            },
        ]
    # Hard questions
    else:
        mock_questions = [
            {
                "id": 7,
                "text": "What measures should governments take to address climate change? Discuss the potential impacts of these policies.",
                "topic": "environment",
                "difficulty": "hard",
                "category": "analytical",
            },
            {
                "id": 8,
                "text": "Discuss the ethical implications of artificial intelligence in healthcare. What safeguards should be put in place?",
                "topic": "technology",
                "difficulty": "hard",
                "category": "analytical",
            },
            {
                "id": 9,
                "text": "How might changing work patterns affect social structures in the future? Consider both positive and negative consequences.",
                "topic": "society",
                "difficulty": "hard",
                "category": "analytical",
            },
        ]

    # Apply topic filter if provided
    if topic:
        mock_questions = [q for q in mock_questions if q["topic"] == topic]

    return SpeakingQuestionsResponse(questions=mock_questions)


@router.get("/listening/passages", response_model=ListeningPassagesResponse)
async def get_listening_passages(
    difficulty: str = Query(..., description="Difficulty level", enum=["easy", "medium", "hard"]),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ListeningPassagesResponse:
    """
    Get listening test passages with questions filtered by difficulty
    """
    # In a real implementation, this would query the database for passages
    # For now, we'll return mock data

    mock_passages = []

    # Easy passages
    if difficulty == "easy":
        mock_passages = [
            {
                "id": 1,
                "title": "Campus Tour",
                "text": "Welcome to our university campus tour. Today, I'll show you the main facilities including the library, student center, and sports complex. The tour will take approximately 30 minutes.",
                "audioUrl": "https://testmateai.com/audio/listening/easy/campus_tour.mp3",
                "duration": 180,
                "questions": [
                    {
                        "id": 101,
                        "text": "What will the tour include?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "Only the library"},
                            {"id": "B", "text": "The library, student center, and sports complex"},
                            {"id": "C", "text": "All university buildings"},
                            {"id": "D", "text": "Classrooms and lecture halls"},
                        ],
                        "correct": {"id": "B", "text": "The library, student center, and sports complex"},
                    },
                    {
                        "id": 102,
                        "text": "How long will the tour take?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "15 minutes"},
                            {"id": "B", "text": "30 minutes"},
                            {"id": "C", "text": "45 minutes"},
                            {"id": "D", "text": "60 minutes"},
                        ],
                        "correct": {"id": "B", "text": "30 minutes"},
                    },
                ],
            }
        ]
    # Medium passages
    elif difficulty == "medium":
        mock_passages = [
            {
                "id": 2,
                "title": "The History of Coffee",
                "text": "In this lecture, we'll explore the fascinating history of coffee, from its discovery in Ethiopia to its global popularity today. We'll examine how coffee cultivation spread across the world and its economic impact throughout history.",
                "audioUrl": "https://testmateai.com/audio/listening/medium/coffee_history.mp3",
                "duration": 300,
                "questions": [
                    {
                        "id": 201,
                        "text": "Where was coffee discovered according to the lecture?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "Brazil"},
                            {"id": "B", "text": "Colombia"},
                            {"id": "C", "text": "Ethiopia"},
                            {"id": "D", "text": "Yemen"},
                        ],
                        "correct": {"id": "C", "text": "Ethiopia"},
                    },
                    {
                        "id": 202,
                        "text": "What aspects of coffee does the lecture primarily discuss?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "Different brewing methods"},
                            {"id": "B", "text": "Health benefits and risks"},
                            {"id": "C", "text": "Cultivation spread and economic impact"},
                            {"id": "D", "text": "Coffee varieties and flavors"},
                        ],
                        "correct": {"id": "C", "text": "Cultivation spread and economic impact"},
                    },
                ],
            }
        ]
    # Hard passages
    else:
        mock_passages = [
            {
                "id": 3,
                "title": "Quantum Computing Applications",
                "text": "Today's advanced seminar will delve into quantum computing applications across various sectors. We'll analyze computational advantages over classical systems, potential breakthroughs in cryptography, and challenges in scaling quantum technologies.",
                "audioUrl": "https://testmateai.com/audio/listening/hard/quantum_computing.mp3",
                "duration": 450,
                "questions": [
                    {
                        "id": 301,
                        "text": "According to the seminar, what is one area where quantum computing shows promise?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "Consumer electronics"},
                            {"id": "B", "text": "Cryptography"},
                            {"id": "C", "text": "Social media"},
                            {"id": "D", "text": "Entertainment systems"},
                        ],
                        "correct": {"id": "B", "text": "Cryptography"},
                    },
                    {
                        "id": 302,
                        "text": "What challenge in quantum computing does the speaker mention?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "Public acceptance"},
                            {"id": "B", "text": "Legal regulations"},
                            {"id": "C", "text": "Scaling technologies"},
                            {"id": "D", "text": "Finding qualified programmers"},
                        ],
                        "correct": {"id": "C", "text": "Scaling technologies"},
                    },
                    {
                        "id": 303,
                        "text": "What comparison does the speaker make in the seminar?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "Quantum vs. classical computing systems"},
                            {"id": "B", "text": "Different quantum hardware manufacturers"},
                            {"id": "C", "text": "Quantum computing in different countries"},
                            {"id": "D", "text": "Theoretical vs. practical applications"},
                        ],
                        "correct": {"id": "A", "text": "Quantum vs. classical computing systems"},
                    },
                ],
            }
        ]

    return ListeningPassagesResponse(passages=mock_passages)


@router.get("/reading/passages", response_model=ReadingPassagesResponse)
async def get_reading_passages(
    difficulty: str = Query(..., description="Difficulty level", enum=["easy", "medium", "hard"]),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ReadingPassagesResponse:
    """
    Get reading test passages with questions filtered by difficulty
    """
    # In a real implementation, this would query the database for passages
    # For now, we'll return mock data

    mock_passages = []

    # Easy passages
    if difficulty == "easy":
        mock_passages = [
            {
                "id": 1,
                "title": "The Benefits of Regular Exercise",
                "text": "Regular exercise has numerous benefits for both physical and mental health. Physical activity helps maintain a healthy weight, reduces the risk of heart disease, and strengthens muscles and bones. Exercise also releases endorphins, which improve mood and reduce stress. Even moderate activity like walking for 30 minutes daily can have significant health benefits.",
                "questions": [
                    {
                        "id": 101,
                        "text": "According to the passage, what are two physical benefits of regular exercise?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "Improved memory and better sleep"},
                            {"id": "B", "text": "Reduced risk of heart disease and stronger muscles"},
                            {"id": "C", "text": "Weight gain and stress reduction"},
                            {"id": "D", "text": "Improved cooking skills and better posture"},
                        ],
                        "correct": {"id": "B", "text": "Reduced risk of heart disease and stronger muscles"},
                    },
                    {
                        "id": 102,
                        "text": "What does the passage suggest about walking?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "It's too easy to provide health benefits"},
                            {"id": "B", "text": "It should be done for at least one hour daily"},
                            {"id": "C", "text": "30 minutes daily can provide significant health benefits"},
                            {"id": "D", "text": "It's only beneficial for elderly people"},
                        ],
                        "correct": {"id": "C", "text": "30 minutes daily can provide significant health benefits"},
                    },
                ],
            }
        ]
    # Medium passages
    elif difficulty == "medium":
        mock_passages = [
            {
                "id": 2,
                "title": "The Impact of Social Media on Society",
                "text": "Social media platforms have fundamentally transformed how people communicate and interact in the 21st century. While these technologies have created unprecedented opportunities for connection across geographical boundaries, they've also raised concerns about privacy, mental health, and the spread of misinformation. Studies have linked excessive social media use to increased feelings of isolation and depression, particularly among younger users. However, these platforms have also enabled social movements, democratized information access, and created new economic opportunities. The challenge for society is balancing the benefits of these technologies while mitigating their potential harms.",
                "questions": [
                    {
                        "id": 201,
                        "text": "What positive impact of social media is mentioned in the passage?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "Improved mental health outcomes"},
                            {"id": "B", "text": "Enhanced privacy protections"},
                            {"id": "C", "text": "Enabling social movements"},
                            {"id": "D", "text": "Reducing isolation"},
                        ],
                        "correct": {"id": "C", "text": "Enabling social movements"},
                    },
                    {
                        "id": 202,
                        "text": "According to the passage, what group is particularly affected by negative mental health impacts of social media?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "Older adults"},
                            {"id": "B", "text": "Younger users"},
                            {"id": "C", "text": "Working professionals"},
                            {"id": "D", "text": "Political activists"},
                        ],
                        "correct": {"id": "B", "text": "Younger users"},
                    },
                    {
                        "id": 203,
                        "text": "What does the passage suggest society needs to do regarding social media?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "Ban social media platforms entirely"},
                            {"id": "B", "text": "Only allow educational content"},
                            {"id": "C", "text": "Balance benefits while reducing harms"},
                            {"id": "D", "text": "Increase regulation without considering benefits"},
                        ],
                        "correct": {"id": "C", "text": "Balance benefits while reducing harms"},
                    },
                ],
            }
        ]
    # Hard passages
    else:
        mock_passages = [
            {
                "id": 3,
                "title": "The Anthropocene Extinction",
                "text": "The Anthropocene extinction, also referred to as the sixth mass extinction, represents an ongoing extinction event attributed primarily to human activity. Unlike previous mass extinctions caused by volcanic eruptions, asteroid impacts, or natural climate shifts, the current biodiversity crisis stems from habitat destruction, overexploitation of resources, pollution, introduction of invasive species, and accelerating climate change. Conservative estimates suggest that current extinction rates are 100 to 1,000 times higher than natural background rates, with potentially millions of species at risk of disappearing within decades. This unprecedented loss of biodiversity threatens ecosystem services essential for human survival, including crop pollination, water purification, and carbon sequestration. While conservation efforts have successfully recovered some species from the brink of extinction, addressing the fundamental drivers of biodiversity loss requires transformative changes in how societies value and interact with natural systems. The scientific consensus increasingly indicates that preventing catastrophic biodiversity loss will necessitate integrated approaches that simultaneously address climate change, reform economic incentive structures, and reimagine humanity's relationship with the natural world.",
                "questions": [
                    {
                        "id": 301,
                        "text": "What distinguishes the Anthropocene extinction from previous mass extinctions according to the passage?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "It is occurring more slowly than previous extinctions"},
                            {"id": "B", "text": "It is primarily caused by human activity"},
                            {"id": "C", "text": "It affects fewer species than previous extinctions"},
                            {"id": "D", "text": "It is limited to marine ecosystems"},
                        ],
                        "correct": {"id": "B", "text": "It is primarily caused by human activity"},
                    },
                    {
                        "id": 302,
                        "text": "According to the passage, how much higher are current extinction rates compared to natural background rates?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "10 to 100 times higher"},
                            {"id": "B", "text": "50 to 500 times higher"},
                            {"id": "C", "text": "100 to 1,000 times higher"},
                            {"id": "D", "text": "1,000 to 10,000 times higher"},
                        ],
                        "correct": {"id": "C", "text": "100 to 1,000 times higher"},
                    },
                    {
                        "id": 303,
                        "text": "What ecosystem services threatened by biodiversity loss are mentioned in the passage?",
                        "type": "true-false",
                        "options": [
                            {"id": "A", "text": "Crop pollination and water purification"},
                            {"id": "B", "text": "Mineral extraction and oil production"},
                            {"id": "C", "text": "Tourism and recreation"},
                            {"id": "D", "text": "Urban development and transportation"},
                        ],
                        "correct": {"id": "A", "text": "Crop pollination and water purification"},
                    },
                    {
                        "id": 304,
                        "text": "What does the passage suggest is necessary to prevent catastrophic biodiversity loss?",
                        "type": "multiple-choice",
                        "options": [
                            {"id": "A", "text": "Focus exclusively on creating wildlife preserves"},
                            {"id": "B", "text": "Integrated approaches addressing multiple interconnected issues"},
                            {"id": "C", "text": "Reintroducing extinct species through genetic technology"},
                            {"id": "D", "text": "Relocating endangered species to other planets"},
                        ],
                        "correct": {
                            "id": "B",
                            "text": "Integrated approaches addressing multiple interconnected issues",
                        },
                    },
                ],
            }
        ]

    return ReadingPassagesResponse(passages=mock_passages)


@router.get("/writing/prompts", response_model=WritingPromptsResponse)
async def get_writing_prompts(
    taskType: str = Query(..., description="Type of writing task", enum=["essay", "letter", "report"]),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> WritingPromptsResponse:
    """
    Get writing prompts filtered by task type
    """
    # In a real implementation, this would query the database for prompts
    # For now, we'll return mock data

    mock_prompts = []

    # Essay prompts
    if taskType == "essay":
        mock_prompts = [
            {
                "id": 1,
                "text": "Some people believe that technology has made life easier and more convenient, while others believe it has made life more complicated and stressful. Discuss both views and give your own opinion.",
                "taskType": "essay",
                "wordLimit": 250,
                "timeLimit": 40,
            },
            {
                "id": 2,
                "text": "In many countries, traditional foods are being replaced by international fast foods. This is having a negative effect on both families and societies. To what extent do you agree or disagree?",
                "taskType": "essay",
                "wordLimit": 250,
                "timeLimit": 40,
            },
            {
                "id": 3,
                "text": "Some people think that governments should focus on reducing environmental pollution and housing problems to help people prevent illness. Others think that more money should be spent on healthcare. Discuss both views and give your opinion.",
                "taskType": "essay",
                "wordLimit": 250,
                "timeLimit": 40,
            },
        ]
    # Letter prompts
    elif taskType == "letter":
        mock_prompts = [
            {
                "id": 4,
                "text": "You recently stayed at a hotel and were dissatisfied with your experience. Write a letter to the hotel manager. In your letter: explain why you stayed at the hotel, describe the problems you encountered, suggest what the hotel should do to improve.",
                "taskType": "letter",
                "wordLimit": 150,
                "timeLimit": 20,
            },
            {
                "id": 5,
                "text": "You want to participate in a community project in your neighborhood. Write a letter to the community coordinator. In your letter: explain which project interests you, describe your relevant skills and experience, ask for information about getting involved.",
                "taskType": "letter",
                "wordLimit": 150,
                "timeLimit": 20,
            },
            {
                "id": 6,
                "text": "You recently purchased an electronic device that does not work properly. Write a letter to the store manager. In your letter: describe what you bought and when, explain the problem with the device, state what action you would like the store to take.",
                "taskType": "letter",
                "wordLimit": 150,
                "timeLimit": 20,
            },
        ]
    # Report prompts
    else:
        mock_prompts = [
            {
                "id": 7,
                "text": "You work for a company that is considering allowing employees to work from home. You have been asked to write a report on the potential benefits and challenges of remote work, and to make recommendations.",
                "taskType": "report",
                "wordLimit": 200,
                "timeLimit": 40,
            },
            {
                "id": 8,
                "text": "Your local government wants to improve public transportation in your city. You have been asked to write a report examining the current issues with public transport and suggesting improvements.",
                "taskType": "report",
                "wordLimit": 200,
                "timeLimit": 40,
            },
            {
                "id": 9,
                "text": "You are a consultant hired by a university to evaluate their student support services. Write a report assessing the current services, identifying any gaps, and recommending improvements.",
                "taskType": "report",
                "wordLimit": 200,
                "timeLimit": 40,
            },
        ]

    return WritingPromptsResponse(prompts=mock_prompts)
