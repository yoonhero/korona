from korokoro.syllable import Syllable

double_consonant_final = {
    'ᆪ': ('ᆨ', 'ᆺ'),
    'ᆬ': ('ᆫ', 'ᆽ'),
    'ᆭ': ('ᆫ', 'ᇂ'),
    'ᆰ': ('ᆯ', 'ᆨ'),
    'ᆱ': ('ᆯ', 'ᆷ'),
    'ᆲ': ('ᆯ', 'ᆸ'),
    'ᆳ': ('ᆯ', 'ᆻ'),
    'ᆴ': ('ᆯ', 'ᇀ'),
    'ᆵ': ('ᆯ', 'ᇁ'),
    'ᆶ': ('ᆯ', 'ᇂ'),
    'ᆹ': ('ᆸ', 'ᆺ'),
    'ㅆ': ('ㅅ', 'ㅅ')
}

NULL_CONSONANT = 'ᄋ'


class Pronouncer(object):
    def __init__(self, text):
        self._syllables = [Syllable(char) for char in text]
        self.pronounced = ''.join([str(c) for c in self.final_substitute()])

    def final_substitute(self):
        for idx, syllable in enumerate(self._syllables):
            try:
                next_syllable = self._syllables[idx+1]
            except IndexError:
                next_syllable = None

            try:
                final_is_before_C = syllable.final and next_syllable.initial not in (
                    None, NULL_CONSONANT)
            except AttributeError:
                final_is_before_C = False

            try:
                final_is_before_V = syllable.final and next_syllable.initial in (
                    None, NULL_CONSONANT)
            except AttributeError:
                final_is_before_V = False

            is_last_syllable = syllable.final and next_syllable is None

            # 1. 받침 ‘ㄲ, ㅋ’, ‘ㅅ, ㅆ, ㅈ, ㅊ, ㅌ’, ‘ㅍ’은 어말 또는 자음 앞에서 각각 대표음 [ㄱ, ㄷ, ㅂ]으로 발음한다.
            # 2. 겹받침 ‘ㄳ’, ‘ㄵ’, ‘ㄼ, ㄽ, ㄾ’, ‘ㅄ’은 어말 또는 자음 앞에서 각각 [ㄱ, ㄴ, ㄹ, ㅂ]으로 발음한다.
            # 3. 겹받침 ‘ㄺ, ㄻ, ㄿ’은 어말 또는 자음 앞에서 각각 [ㄱ, ㅁ, ㅂ]으로 발음한다.
            # <-> 단, 국어의 로마자 표기법 규정에 의해 된소리되기는 표기에 반영하지 않으므로 제외.
            if is_last_syllable or final_is_before_C:
                if (syllable.final in ['ᆩ', 'ᆿ', 'ᆪ', 'ᆰ']):
                    syllable.final = 'ᆨ'
                elif (syllable.final in ['ᆺ', 'ᆻ', 'ᆽ', 'ᆾ', 'ᇀ']):
                    syllable.final = 'ᆮ'
                elif (syllable.final in ['ᇁ', 'ᆹ', 'ᆵ']):
                    syllable.final = 'ᆸ'
                elif (syllable.final in ['ᆬ']):
                    syllable.final = 'ᆫ'
                elif (syllable.final in ['ᆲ', 'ᆳ', 'ᆴ']):
                    syllable.final = 'ᆯ'
                elif (syllable.final in ['ᆱ']):
                    syllable.final = 'ᆷ'

            # 4. 받침 ‘ㅎ’의 발음은 다음과 같다.
            if syllable.final in ['ᇂ', 'ᆭ', 'ᆶ']:
                without_ㅎ = {
                    'ᆭ': 'ᆫ',
                    'ᆶ': 'ᆯ',
                    'ᇂ': None
                }

                if next_syllable:
                    # ‘ㅎ(ㄶ, ㅀ)’ 뒤에 ‘ㄱ, ㄷ, ㅈ’이 결합되는 경우에는, 뒤 음절 첫소리와 합쳐서 [ㅋ, ㅌ, ㅊ]으로 발음한다.
                    # ‘ㅎ(ㄶ, ㅀ)’ 뒤에 ‘ㅅ’이 결합되는 경우에는, ‘ㅅ’을 [ㅆ]으로 발음한다.
                    if next_syllable.initial in ['ᄀ', 'ᄃ', 'ᄌ', 'ᄉ']:
                        change_to = {'ᄀ': 'ᄏ', 'ᄃ': 'ᄐ', 'ᄌ': 'ᄎ', 'ᄉ': 'ᄊ'}
                        syllable.final = without_ㅎ[syllable.final]
                        next_syllable.initial = change_to[next_syllable.initial]
                    # 3. ‘ㅎ’ 뒤에 ‘ㄴ’이 결합되는 경우에는, [ㄴ]으로 발음한다.
                    elif next_syllable.initial in ['ᄂ']:
                        # TODO: [붙임] ‘ㄶ, ㅀ’ 뒤에 ‘ㄴ’이 결합되는 경우에는, ‘ㅎ’을 발음하지 않는다.
                        if (syllable.final in ['ᆭ', 'ᆶ']):
                            syllable.final = without_ㅎ[syllable.final]
                        else:
                            syllable.final = 'ᆫ'
                    # 4. ‘ㅎ(ㄶ, ㅀ)’ 뒤에 모음으로 시작된 어미나 접미사가 결합되는 경우에는,
                    # ‘ㅎ’을 발음하지 않는다.
                    elif next_syllable.initial == NULL_CONSONANT:
                        if (syllable.final in ['ᆭ', 'ᆶ']):
                            if syllable.final == 'ᆭ':
                                syllable.final = 'ᆫ'
                            elif syllable.final == 'ᆶ':
                                syllable.final = 'ᆯ'
                        else:
                            syllable.final = None
                    elif next_syllable.initial == 'ᄅ':
                        if (syllable.final == 'ᆶ'):
                            syllable.final = 'ᆯ'
                    else:
                        if (syllable.final == 'ᇂ'):
                            syllable.final = None
                        else:
                            syllable.final = without_ᄒ[syllable.final] # easy error handle but maybe not correct..?
                            
                else:
                    if (syllable.final == 'ᇂ'):
                        syllable.final = None
                    else:
                        syllable.final = without_ᄒ[syllable.final]

            # 6. 겹받침이 모음으로 시작된 조사나 어미, 접미사와 결합되는 경우에는,
            # 뒤엣것만을 뒤 음절 첫소리로 옮겨 발음한다.(이 경우, ‘ㅅ’은 된소리로 발음함.)
            if syllable.final in double_consonant_final and next_syllable.initial == NULL_CONSONANT:

                double_consonant = double_consonant_final[syllable.final]
                syllable.final = double_consonant[0]
                next_syllable.initial = next_syllable.final_to_initial(
                    double_consonant[1])
            # 5. 홑받침이나 쌍받침이 모음으로 시작된 조사나 어미, 접미사와 결합되는 경우에는,
            # 제 음가대로 뒤 음절 첫소리로 옮겨 발음한다.
            if next_syllable and final_is_before_V:
                # do nothing if final is ᆼ or null
                if (next_syllable.initial == NULL_CONSONANT and syllable.final not in ["ᆼ", None]):
                    next_syllable.initial = next_syllable.final_to_initial(
                        syllable.final)
                    syllable.final = None

            if syllable.final in double_consonant_final.keys():
                double_consonant = double_consonant_final[syllable.final]
                # 제11항  겹받침 'ㄺ, ㄻ, ㄿ'은 어말 또는 자음 앞에서 각각 [ㄱ, ㅁ, ㅂ]으로 발음한다.
                if double_consonant[0] == 'ㄹ' and double_consonant[1] in ['ㄱ', 'ㅁ', 'ㅍ']:
                    syllable.final = double_consonant[1]
                # 제10항  겹받침 'ㄳ', 'ㄵ', 'ㄼ, ㄽ, ㄾ', 'ㅄ'은 어말 또는 자음 앞에서 각각 [ㄱ, ㄴ, ㄹ, ㅂ]으로 발음한다.
                # 다만, ‘밟-’은 자음 앞에서 [밥]으로 발음하고, ‘넓-’은 다음과 같은 경우에 [넙]으로 발음한다.
                elif ( double_consonant == 'ㄼ') and ((syllable=="밟" and next_syllable.initial != NULL_CONSONANT)  or (syllable=="넓") ):
                    syllable.final = double_consonant[1]
                elif double_consonant in ['ㄳ', 'ㄵ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㅄ']:
                    syllable.final = double_consonant[0]

        return self._syllables
