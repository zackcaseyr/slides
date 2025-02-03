from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.contrib import messages
from django.http import FileResponse
from .models import Class, Topic, Slide
from .forms import TopicWithSlidesForm, SlideFormSet
from .utils import create_topic_pdf

# Class Views
class ClassListView(ListView):
    model = Class
    template_name = 'topics/class_list.html'
    context_object_name = 'classes'

class ClassDetailView(DetailView):
    model = Class
    template_name = 'topics/class_detail.html'
    context_object_name = 'class'

class ClassCreateView(CreateView):
    model = Class
    template_name = 'topics/class_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('class-list')

class ClassUpdateView(UpdateView):
    model = Class
    template_name = 'topics/class_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('class-list')

class ClassDeleteView(DeleteView):
    model = Class
    template_name = 'topics/class_confirm_delete.html'
    success_url = reverse_lazy('class-list')

# Topic Views
class TopicListView(ListView):
    model = Topic
    template_name = 'topics/topic_list.html'
    context_object_name = 'topics'

class TopicDetailView(DetailView):
    model = Topic
    template_name = 'topics/topic_detail.html'
    context_object_name = 'topic'

class TopicCreateView(CreateView):
    model = Topic
    template_name = 'topics/topic_form.html'
    fields = ['class_obj', 'title', 'description']
    success_url = reverse_lazy('topic-list')

class TopicUpdateView(UpdateView):
    model = Topic
    template_name = 'topics/topic_form.html'
    fields = ['class_obj', 'title', 'description']
    success_url = reverse_lazy('topic-list')

class TopicDeleteView(DeleteView):
    model = Topic
    template_name = 'topics/topic_confirm_delete.html'
    success_url = reverse_lazy('topic-list')

class TopicWithSlidesCreateView(CreateView):
    model = Topic
    form_class = TopicWithSlidesForm
    template_name = 'topics/topic_with_slides_form.html'
    success_url = reverse_lazy('topic-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['slides_formset'] = modelformset_factory(
                Slide, 
                form=SlideFormSet,
                extra=self.request.POST.get('extra_slides', 1),
                can_delete=True
            )(self.request.POST, self.request.FILES, prefix='slides')
        else:
            context['slides_formset'] = modelformset_factory(
                Slide, 
                form=SlideFormSet,
                extra=1,
                can_delete=True
            )(queryset=Slide.objects.none(), prefix='slides')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        slides_formset = context['slides_formset']

        if slides_formset.is_valid():
            self.object = form.save()
            slides = slides_formset.save(commit=False)
            
            # Set the topic for each slide and save
            for slide in slides:
                slide.topic = self.object
                slide.save()
            
            # Handle deleted slides
            for slide in slides_formset.deleted_objects:
                slide.delete()
                
            messages.success(self.request, 'Topic and slides created successfully!')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error creating the topic and slides.')
        return super().form_invalid(form)

class TopicPDFView(View):
    def get(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        buffer = create_topic_pdf(topic)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f"{topic.title.replace(' ', '_')}_slides.pdf"
        )

# Presentation View
class PresentationView(DetailView):
    model = Topic
    template_name = 'topics/presentation.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slides'] = self.object.slides.all().order_by('order')
        return context

# Slide Views
class SlideListView(ListView):
    model = Slide
    template_name = 'topics/slide_list.html'
    context_object_name = 'slides'

class SlideDetailView(DetailView):
    model = Slide
    template_name = 'topics/slide_detail.html'
    context_object_name = 'slide'

class SlideCreateView(CreateView):
    model = Slide
    template_name = 'topics/slide_form.html'
    fields = ['topic', 'title', 'content', 'image', 'video', 'order']
    success_url = reverse_lazy('slide-list')

class SlideUpdateView(UpdateView):
    model = Slide
    template_name = 'topics/slide_form.html'
    fields = ['topic', 'title', 'content', 'image', 'video', 'order']
    success_url = reverse_lazy('slide-list')

class SlideDeleteView(DeleteView):
    model = Slide
    template_name = 'topics/slide_confirm_delete.html'
    success_url = reverse_lazy('slide-list')