from django.shortcuts import render,redirect,HttpResponse
from .models import Item,Review,Old_Training_data,Training_Review
from .forms import ReviewForm,Old_Form,AdminReviewForm
from datetime import datetime
from django.contrib.auth import authenticate,login
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pandas as pd
import numpy as np
import re
from .forms import UserForm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from django.forms import formset_factory

# Create your views here.

def showItems(request):
    items=Item.objects.all()
    return render(request,'review_classifier/index.html',{'items':items})

def viewitem(request,pk):
    item = Item.objects.get(pk=pk)
    if request.method=='POST':
        form=ReviewForm(data=request.POST)
        if form.is_valid():
            review_form=form.save(commit=False)
            review_form.item=item
            review_form.timestamp=datetime.now()
            review_form.review_type=True
            review_form.save()
        return redirect('home:showitems')
    else:
        form=ReviewForm()
        return render(request,'review_classifier/product_review.html',{'item':item,'form':form})
def makeCorpus(request):
    # Importing the data
    dataset = pd.read_csv('C://Users//ASUS//Desktop//Natural_Language_Processing//Restaurant_Reviews.tsv', delimiter='\t', quoting=3)
    #CLEAN THE DATASET
    corpus = []
    for i in range(0, 1000):
        review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
        review = review.lower()
        review = review.split()
        ps = PorterStemmer()
        review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.append(review)
    #sending Corpus to Session
    request.session['corpus']=corpus
    return redirect('review_classifier:showitems')


def predictNewReviews(request):
    if request.method=='GET':
        # creating the bag of words model
        dataset = pd.read_csv('C://Users//ASUS//Desktop//Natural_Language_Processing//Restaurant_Reviews.tsv',delimiter='\t', quoting=3)

        corpus=request.session['corpus']
        cv = CountVectorizer(max_features=1500)
        X = cv.fit_transform(corpus).toarray()
        y = dataset.iloc[:, 1].values

        # Splitting to test and train
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # getting reviews of user
        review_objs = Review.objects.all()
        print('hello1')
        for i in review_objs:
            review_object = str(i.review)
            review_object = re.sub('[^a-zA-Z]', ' ', review_object)
            review_object = review_object.lower()
            review_object = review_object.split()
            ps1 = PorterStemmer()
            review_object = [ps1.stem(word) for word in review_object if not word in set(stopwords.words('english'))]
            review_object = ' '.join(review_object)
            corpus.append(review_object)

        # Creating new Bag of words model
        cv = CountVectorizer(max_features=1500)
        X = cv.fit_transform(corpus).toarray()
        print(np.shape(X))
        X_new = X[1000:]

        # Fitting the data into the training set
        classifier = GaussianNB()
        classifier.fit(X_train, y_train)
        print('hello')

        # Predicting data through test set
        y_pred = classifier.predict(X_new)
        j = 0
        for i in review_objs:
            i.review_type = y_pred[j]
            j = j + 1
            i.save()
        temp_obj=Review.objects.all()
        list=[]
        for object in temp_obj:
            form=AdminReviewForm(instance=object)
            list.append(form)
        return render(request,'review_classifier/dashboard.html',{'form':list})
    else:
        objects=Review.objects.filter(is_verified=False)
        print(objects)
        temp1=request.POST.get('is_verified')
        print(request.POST)
        combined_object=zip(objects,request.POST['is_verified'],request.POST['review_type'])
        for object,value,review_value in combined_object:
            if value is 'off':
                object.is_verified=False
            else:
                object.is_verified=True
            if (review_value is 'off'):
                object.review_type = False
            else:
                object.review_type = True

            object.save()
        return render(request,'review_classifier/dashboard.html')

def loginFunction(request):
    if request.method =='POST':
        form=UserForm(data=request.POST)
        username=form.username
        password=form.password
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                redirect('home:showitems')
        else:
            return HttpResponse("Login Failed INvalid Credentials")
    else:
        form=UserForm()
        return  render(request,'review_classifier/login.html',{'form':form})
'''def insertData(request):
    dataset = pd.read_csv('C://Users//ASUS//Desktop//Natural_Language_Processing//Restaurant_Reviews.tsv',delimiter='\t', quoting=3)

    for i in range(0,1000):
        form=Old_Form()
        saveform=form.save(commit=False)
        print(str(dataset['Review'][i]))
        saveform.review = str(dataset['Review'][i])
        saveform.review_type = dataset['Liked'][i]
        saveform.save()
    print("Successfull")
    return HttpResponse("Your Data inserted successfully")

'''