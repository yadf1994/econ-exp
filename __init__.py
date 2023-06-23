from random import randrange
from otree.api import *
import random,json
from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Page,
    Currency as c,
    currency_range,
)
doc = """
EXPERIENCE
"""

class C(BaseConstants):
    NAME_IN_URL = 'test1'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 50
    COLOR_DISPLAYED_DURATION = 1.5
    RESULTS_DURATION = 10
    COLOR_CHOICES_DURATION = 30
    TOTAL_ROUND_DURATION = COLOR_DISPLAYED_DURATION + COLOR_CHOICES_DURATION
    A_PARTAGER = 10

    COLORS = ['#000000', '#808080', '#C0C0C0', '#FFFFFF', '#800000', '#FF0000', '#808000', '#FFFF00',
              '#008000', '#00FF00', '#008080', '#00FFFF', '#000080', '#0000FF', '#800080', '#FF00FF',
              '#F0F8FF', '#FAEBD7', '#00FFFF', '#7FFFD4', '#F0FFFF', '#F5F5DC', '#FFE4C4', '#000000',
              '#FFEBCD', '#0000FF', '#8A2BE2', '#A52A2A', '#DEB887', '#5F9EA0', '#7FFF00', '#D2691E',
              '#FF7F50', '#6495ED', '#FFF8DC', '#DC143C', '#00FFFF', '#00008B', '#008B8B', '#B8860B',
              '#A9A9A9', '#006400', '#BDB76B', '#8B008B', '#556B2F', '#FF8C00', '#9932CC', '#8B0000',
              '#E9967A', '#8FBC8F', '#483D8B', '#2F4F4F', '#00CED1', '#9400D3', '#FF1493', '#00BFFF',
              '#696969', '#1E90FF', '#B22222', '#FFFAF0', '#228B22', '#FF00FF', '#DCDCDC', '#F8F8FF',
              '#FFD700', '#DAA520', '#808080', '#008000', '#ADFF2F', '#F0FFF0', '#FF69B4', '#CD5C5C',
              '#4B0082', '#FFFFF0', '#F0E68C', '#E6E6FA', '#FFF0F5', '#7CFC00', '#FFFACD', '#ADD8E6',
              '#F08080', '#E0FFFF', '#FAFAD2', '#90EE90', '#D3D3D3', '#FFB6C1', '#FFA07A', '#20B2AA',
              '#87CEFA', '#778899', '#B0C4DE', '#FFFFE0', '#00FF00', '#32CD32', '#FAF0E6', '#FF00FF',
              '#800000', '#66CDAA', '#0000CD', '#BA55D3', '#9370DB', '#3CB371', '#7B68EE', '#00FA9A',
              '#48D1CC', '#C71585', '#191970', '#F5FFFA', '#FFE4E1', '#FFE4B5', '#FFDEAD', '#000080',
              '#FDF5E6', '#808000', '#6B8E23', '#FFA500', '#FF4500', '#DA70D6', '#EEE8AA', '#98FB98',
              '#AFEEEE', '#DB7093', '#FFEFD5', '#FFDAB9', '#CD853F', '#FFC0CB', '#DDA0DD', '#B0E0E6',
              '#800080', '#FF0000', '#BC8F8F', '#416']

def creating_session(self):
    if self.round_number == 1:
        # On mélange les joueurs pour qu'ils soient regroupés de manière aléatoire
        self.group_randomly()

    for g in self.get_groups():
        # Choix de couleur à présenter brièvement
        previous_color = random.choice(C.COLORS)
        color_choices = random.sample(C.COLORS, 4)
        color_choices.append(previous_color)
        # random.shuffle(color_choices)
        g.attaque=random.choice([True,False])
        g.option_att=random.randrange(4)+1 if g.attaque else 0
        g.n_votes_en_plus=random.randrange(4)+1 if g.attaque else 0

        # Attribution de la liste de couleurs à ce groupe
        g.set_color_list(color_choices)
        ctr =  self.session.config['treatment']
        if ctr < 0:
            ctr=random.choice([0,1])
            if ctr > 0:
                ctr=random.choice([1,2])
        for p in g.get_players():
            p.treatment=ctr

    if False: #for p in self.get_players()
        # Récupération de la couleur à présenter brièvement
        p.previous_color = p.group.color_choices[-1]

        # Récupération des 4 couleurs de choix pour ce joueur
        for i in range(4):
            setattr(p, 'color{}'.format(i + 1), p.group.color_choices[i])

        # Envoi des couleurs et des durées de présentation aux pages des joueurs
        previous_color = p.group.color_choices[-1]
        choices = p.group.color_choices[:-1]
        p.participant.vars['color_displayed'] = previous_color
        p.participant.vars['time_displayed'] = C.COLOR_DISPLAYED_DURATION
        for i in range(4):
            p.participant.vars['color{}'.format(i + 1)] = choices[i]
            p.participant.vars['time{}'.format(i + 1)] = C.COLOR_CHOICES_DURATION


def nplosses_winners(group,opts):
    losses=[]
    wins=[]
    for o in opts: losses.append(0)
    for o in opts: wins.append(0)
    att=""
    pchoices=[]
    for p in group.get_players():
        classed_opts=[int(op) for op in p.classed_colors.split(',') if int(op) in opts] if not (p.classed_colors is None or p.classed_colors=='') else []
        pchoices.append(classed_opts)
    if group.attaque:
        att=", attacked option %d with %d votes"%(group.option_att,group.n_votes_en_plus)
        for a in range(group.n_votes_en_plus):
            if group.option_att in opts: pchoices.append([group.option_att])
    for i,o in enumerate(opts):
        for i2,o2 in enumerate(opts):
            if o != o2:
                nvotes_o=0; nvotes_o2=0
                for classed_opts in pchoices:
                    copindex=classed_opts.index(o) if o in classed_opts else len(opts)
                    copindex2=classed_opts.index(o2) if o2 in classed_opts else len(opts)
                    if copindex<copindex2: nvotes_o+=1
                    if copindex2<copindex: nvotes_o2+=1
                if nvotes_o <= nvotes_o2: losses[i]+=1
                else: wins[i]+=1
                # if nvotes_o2 <= nvotes_o: losses[i2]+=1

    zeroloss=[]
    wincount=[]
    print("Round %d, group %d; Losses per option:"%(group.round_number,group.id_in_subsession),losses,att)
    # condorcet_winners(group,opts)
    if len(opts)==4: group.votes_par_option=','.join([str(o) for o in wins])
    for h,l in enumerate(losses):
        if l == 0:
            zeroloss.append(opts[h])
            wincount.append(wins[h])
    if len(wincount)>0: group.majority_nvotes=max(wincount)
    # elif group.field_maybe_none("majority_nvotes") is None: group.majority_nvotes=max(wins)
    return zeroloss

def borda_winners(group,opts):
    wins=[]
    for o in opts: wins.append(0)
    att=""
    pchoices=[]
    for p in group.get_players():
        classed_opts=[int(op) for op in p.classed_colors.split(',') if int(op) in opts] if not (p.classed_colors is None or p.classed_colors=='') else []
        pchoices.append(classed_opts)
    if group.attaque:
        att=", attacked option %d with %d votes"%(group.option_att,group.n_votes_en_plus)
        for a in range(group.n_votes_en_plus):
            if group.option_att in opts: pchoices.append([group.option_att])
    for i,o in enumerate(opts):
        for classed_opts in pchoices:
            copindex=classed_opts.index(o) if o in classed_opts else len(opts)
            wins[i]+=len(opts)-copindex
    cwinners=[]
    print("Round %d, group %d; Borda scores:"%(group.round_number,group.id_in_subsession),wins,att)
    maxnwins=max(wins)
    group.votes_par_option=','.join([str(o) for o in wins])
    group.majority_nvotes=maxnwins # if maxnwins > 0 else 1
    for h,w in enumerate(wins):
        if w == maxnwins and w > 0:
            cwinners.append(opts[h])
    return cwinners

def fewest_toprank(group,opts):
    toprank=[]
    for o in opts: toprank.append(0)
    att=""
    pchoices=[]
    for p in group.get_players():
        classed_opts=[int(op) for op in p.classed_colors.split(',') if int(op) in opts] if not (p.classed_colors is None or p.classed_colors=='') else []
        pchoices.append(classed_opts)
    if group.attaque:
        att=", attacked option %d with %d votes"%(group.option_att,group.n_votes_en_plus)
        for a in range(group.n_votes_en_plus):
            if group.option_att in opts: pchoices.append([group.option_att])
    for i,o in enumerate(opts):
        for classed_opts in pchoices:
            copindex=classed_opts.index(o) if o in classed_opts else len(opts)
            if copindex == 0: toprank[i]+=1
    cftr=[]
    print("Round %d, group %d; toprank count:"%(group.round_number,group.id_in_subsession),toprank,att)
    mintr=min(toprank)
    for h,w in enumerate(toprank):
        if w == mintr:
            cftr.append(opts[h])
    return cftr

class Subsession(BaseSubsession):
    pass

class ColorChoice1(Page):
    @staticmethod
    def is_displayed(player):
        return player.treatment==0
    timeout_seconds = C.COLOR_CHOICES_DURATION
    form_model = 'player'
    form_fields = ['color_choice']

class ColorChoice2(Page):
    @staticmethod
    def is_displayed(player):
        return player.treatment>0
    timeout_seconds = C.COLOR_CHOICES_DURATION
    form_model = 'player'
    form_fields = ['classed_colors']
    def vars_for_template(player):
        colors = player.group.color_list.split(',')
        return {
            'color_choices': [[i+1,h] for (i,h) in enumerate(colors[:-1])],
            'tr_text': ['WOODSIRV','Borda'][player.treatment-1],
        }

class Group(BaseGroup):
    # ... Autres méthodes et attributs de la classe ...
    color_list = models.LongStringField()
    majority_choices=models.StringField()
    majority_nvotes=models.IntegerField()
    votes_par_option=models.StringField()
    attaque=models.BooleanField()
    option_att=models.IntegerField()
    n_votes_en_plus=models.IntegerField()
    #color_choices = models.LongStringField()
    method = models.StringField()
    def set_color_list(self, color_list):
        self.color_list = ','.join(color_list)

    def generate_color_list(self):
        return self.color_list

def color_choice_choices(player):
    #print(player.session.config['treatment'])
    colors=player.group.color_list.split(',')
    return [[i+1,h] for (i,h) in enumerate(colors[:-1])]

class Player(BasePlayer):

    treatment=models.IntegerField()
    color_choice=models.IntegerField(label='Choisissez la couleur')
    classed_colors=models.StringField()

# PAGES
class ColorDisplayed(Page):
    timeout_seconds = C.COLOR_DISPLAYED_DURATION
    def vars_for_template(player):
        colors = player.group.color_list.split(',')
        return {
            'previous_color': colors[-1],
        }
class Results(Page):
    timeout_seconds = C.RESULTS_DURATION
    def is_displayed(player):
        return True #player.treatment<=1
    def vars_for_template(player):
        group=player.group
        colors = group.color_list.split(',')
        winnercolors=[]
        votes=[int(v) for v in group.votes_par_option.split(',')]
        # if group.majority_nvotes>0:
        winneropts=[int(o) for o in group.majority_choices.split(',')] if not group.field_maybe_none('majority_choices') is None and group.majority_choices != '' else []
        if len(winneropts)>0:
            for w in winneropts:
                winnercolors.append({'color':colors[w-1], 'nvotes':votes[w-1]})
        
        return {
            'previous_color': colors[-1],
            'winnercolors': winnercolors,
            'n_winners': len(winnercolors),
        }

# Déterminer la page suivante en fonction de la méthode de vote choisie

class MyWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        players=group.get_players()
        if players[0].treatment==0:
            votes=[0]*4
            for p in group.get_players():
                if p.color_choice>0: votes[p.color_choice-1]+=1
            if group.attaque:
                votes[group.option_att-1]+=group.n_votes_en_plus
            maxvotes=0
            for v in votes:
                if v>maxvotes: maxvotes=v
            group.majority_nvotes=maxvotes
            group.votes_par_option=','.join([str(o) for o in votes])
            winneropts=[]
            for (i,v) in enumerate(votes):
                if v==maxvotes and v > 0: winneropts.append(i+1)
            group.majority_choices=','.join([str(o) for o in winneropts])
            winners=[]
            for p in group.get_players():
                if p.color_choice in winneropts: winners.append(p)
            mapart=C.A_PARTAGER/len(winners) if len(winners)>0 else 0
            for p in winners:
                p.payoff=mapart
        else:
            options=list(range(1,5))
            initoptions=[]
            for o in options: initoptions.append(o)
            if players[0].treatment==1:
                step=0
                while len(options)>1: #WoodSIRV
                    step+=1
                    prevoptions=[]
                    for o in options: prevoptions.append(o)
                    # cwinners=condorcet_winners(group,options)
                    cwinners=nplosses_winners(group,options)
                    print("Round %d, group %d; WoodSIRV step %d, cwinners : "%(group.round_number,group.id_in_subsession,step),cwinners, "options:",options)
                    if(len(cwinners)) != 1:
                        toeliminate=fewest_toprank(group,options)
                        if toeliminate!=options or step==1:
                            for t in toeliminate: options.pop(options.index(t))
                        if options == prevoptions:
                            print("Round %d, group %d; Step %d: no one is eliminated, breaking"%(group.round_number,group.id_in_subsession,step))
                            break
                    else:
                        options=cwinners
                print("Round %d, group %d; WoodSIRV winners:"%(group.round_number,group.id_in_subsession),options)
                group.majority_choices=','.join([str(o) for o in options])
            else: #BORDA
                cwinners=borda_winners(group,options)
                print("Round %d, group %d; Borda winners:"%(group.round_number,group.id_in_subsession),cwinners)
                group.majority_choices=','.join([str(o) for o in cwinners])
            weights=[]
            for p in players: weights.append(0)
            winneropts=[int(o) for o in group.majority_choices.split(',')] if group.majority_choices != '' else []
            options=initoptions
            for ip,p in enumerate(players):
                classed_opts=[int(op) for op in p.classed_colors.split(',')] if not (p.classed_colors is None or p.classed_colors=='') else []
                bestrank=len(options)
                for wo in winneropts:
                    if wo in classed_opts and classed_opts.index(wo)+1<bestrank: bestrank=classed_opts.index(wo)+1
                weights[ip]=len(options)-bestrank
            for ip,p in enumerate(players):
                p.payoff=C.A_PARTAGER*weights[ip]/sum(weights) if sum(weights) > 0 else C.A_PARTAGER/len(players) #0
                print("Round %d; group %d; player %d; classed [%s]; weight %d for winner_options [%s], gain %f"%(p.round_number,group.id_in_subsession,p.id_in_group,p.classed_colors,weights[ip],','.join([str(w) for w in winneropts]),p.payoff))
            



page_sequence = [
        ColorDisplayed,
        ColorChoice1,
        ColorChoice2,
        MyWaitPage,
        Results
    ]