from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# from django.http import HttpResponse

# Create your views here.
def index(request):
    """
    질문 목록 출력
    """
    page = request.GET.get('page', '1')

    question_list = Question.objects.order_by('-create_date')

    #페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list' : page_obj} # {key, value}
    return render(request, 'pybo/question_list.html', context)
    # return HttpResponse("Hello World")

def detail(request, question_id):
    """
    질문 내용 출력
    """
    question = get_object_or_404(Question, pk = question_id)
    context = {'question' : question} # {key, value}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    답변 등록
    """
    question = get_object_or_404(Question, pk = question_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id = question.id)
    else:
        form = AnswerForm()

    context = {'question' : question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit = False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()

    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    질문 수정
    """
    question = get_object_or_404(Question, pk = question_id)
    # 로그인한 작성자와 글 작성자가 일치하지 않을 때 메세지 보내기
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id = question.id)

    if request.method == "POST":
        # instance = 생성된 복제 / 할당된 구역
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id = question.id)
    else:
        form = QuestionForm(instance=question)

    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    질문 삭제
    """
    # 삭제 권한이 없을 때 메세지 뿅
    question = get_object_or_404(Question, pk = question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id = question.id)
    #삭제
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    답변 수정
    """
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id = answer.question.id)

    if request.method == "POST":
        # instance = 생성된 복제 / 할당된 구역
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id = answer.question.id)
    else:
        form = AnswerForm(instance=answer)

    context = {'answer' : answer, 'form' : form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    답변 삭제
    """
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id = answer.question.id)
