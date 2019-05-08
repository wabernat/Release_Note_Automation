
def prompt(questions, prmpt='> '):
    return {
        question: input('{} {}'.format(
            question.capitalize(),
            prmpt
        )) for question in questions
    }
