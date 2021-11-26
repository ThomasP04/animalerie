from django.shortcuts import render
from django.shortcuts import redirect
from .models import Animal
from .models import Equipement
from django.shortcuts import render, get_object_or_404
from .forms import MoveForm
from django.contrib import messages


def post_list(request):
    animals = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'jeu/post_list.html', {'animals': animals, 'equipements': equipements})

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    form = MoveForm(request.POST, instance=animal)
    print (form)
    if form.is_valid():
        form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        print(ancien_lieu, nouveau_lieu, animal.etat)

        if nouveau_lieu.id_equip=="mangeoire":
            if animal.etat!='affame':
                messages.add_message(request, messages.INFO, 'Cet animal n a pas faim')
            elif nouveau_lieu.disponibilite!="libre":
                messages.add_message(request, messages.INFO, 'La mangeoire est occupée')
            else:
                animal.etat="repus"
                animal.save()
                nouveau_lieu.disponibilite="occupe"
                nouveau_lieu.save()
                messages.add_message(request, messages.INFO, 'Cet animal a été déplacé dans la mangeoire')

        elif nouveau_lieu.id_equip=="roue":
            if animal.etat!='repus':
                messages.add_message(request, messages.INFO, 'Cet animal n a pas besoin de faire du sport')
            elif nouveau_lieu.disponibilite!="libre":
                messages.add_message(request, messages.INFO, 'La roue est occupée')
            else:
                ancien_lieu.disponibilite="libre"
                ancien_lieu.save()
                animal.etat="fatigue"
                animal.save()
                nouveau_lieu.disponibilite = "occupe"
                nouveau_lieu.save()
                messages.add_message(request, messages.INFO, 'Cet animal a été déplacé dans la roue')

        elif nouveau_lieu.id_equip=="nid":
            if animal.etat!='fatigue':
                messages.add_message(request, messages.INFO, 'Cet animal n a pas besoin de dormir')
            elif nouveau_lieu.disponibilite!="libre":
                messages.add_message(request, messages.INFO, 'Le nid est occupé')
            else:
                ancien_lieu.disponibilite="libre"
                ancien_lieu.save()
                animal.etat="endormi"
                animal.save()
                nouveau_lieu.disponibilite = "occupe"
                nouveau_lieu.save()
                messages.add_message(request, messages.INFO, 'Cet animal a été déplacé dans le nid')

        elif nouveau_lieu.id_equip=="litiere":
            if animal.etat != 'endormi':
                messages.add_message(request, messages.INFO, 'Cet animal n a pas besoin de se réveiller')
            else:
                ancien_lieu.disponibilite="libre"
                ancien_lieu.save()
                animal.etat="affame"
                animal.save()
                nouveau_lieu.disponibilite = "libre"
                nouveau_lieu.save()
                messages.add_message(request, messages.INFO, 'Cet animal a été déplacé dans la litière')
        else:
            print('message')
            messages.add_message(request, messages.INFO, 'Désolé, vous ne pouvez pas déplacer cet animal à cet endroit.')
        
        return redirect('animal_detail', id_animal=id_animal)
    else:
        lieu=animal.lieu
        return render(request,
                  'jeu/animal_detail.html',
                  {'animal': animal, 'lieu': lieu, 'form': form})