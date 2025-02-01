from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Question,Profile,UserScore
from django.contrib.auth.models import User
from .forms import RegisterForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Assurer que le mot de passe est crypté
            user.save()

            # Créer et associer un profil à l'utilisateur
            user_profile = Profile.objects.create(user=user, name=form.cleaned_data['name'])

            login(request, user)  # Connecter l'utilisateur après l'inscription
            return redirect('question_view', question_id=1)  # Rediriger vers la première question
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})




@login_required
def score_view(request):
    # Récupérer le score de l'utilisateur connecté
    user_score = UserScore.objects.filter(user=request.user).last()  # Dernier score enregistré

    return render(request, 'score.html', {'score': user_score.score, 'user_name': request.user.username})



"""
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('question_view', question_id=1)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
"""
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('question_view', question_id=1)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')




@login_required
def question_view(request, question_id):
    # Récupérer la question actuelle
    question = get_object_or_404(Question, id=question_id)

    # Si l'utilisateur n'a pas encore de score dans la session, l'initialiser à 0
    if 'score' not in request.session:
        request.session['score'] = 0

    result = None

    if request.method == "POST":
        # Récupérer la réponse soumise par l'utilisateur
        reponse = request.POST.get("reponse")

        # Vérifier si la réponse est correcte
        if reponse == question.bonne_reponse:
            result = "Bravo ! C'est la bonne réponse."
            request.session['score'] += 1  # Ajouter 1 au score pour une bonne réponse
        else:
            result = f"Faux ! {question.explication}"  # Afficher l'explication de l'erreur

        # Chercher la question suivante
        next_question = Question.objects.filter(id__gt=question_id).first()

        if next_question is None:  # Si c'est la dernière question
            user_name = request.user.profile.name  # Récupérer le nom de l'utilisateur
            total_score = request.session['score']

            # Enregistrer le score total dans UserScore
            UserScore.objects.create(user=request.user, score=total_score)

            # Réinitialiser le score dans la session (si nécessaire)
            request.session['score'] = 0

            # Afficher le score à l'utilisateur
            return render(request, 'score.html', {'score': total_score, 'user_name': user_name})

        # Si ce n'est pas la dernière question, rediriger vers la question suivante
        return render(request, "question.html", {"question": question, "result": result, "next_question": next_question})

    return render(request, "question.html", {"question": question, "result": result})
