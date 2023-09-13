from time import perf_counter
prog_start = perf_counter()


class CalcTime:

    all_time = dict()
    last_interval = 0

    def __call__(self, stage=None):
        if stage in ("last", -1):
            raise KeyError()

        def decorator(f):
            def wrapper(*args, **kwargs):
                start = perf_counter()
                res = f(*args, **kwargs)
                self.last_interval = perf_counter() - start
                if stage:
                    if self.__have_stage(stage):
                        self.all_time[stage].append(self.last_interval)
                    else:
                        self.__add_new_stage(stage)
                return res
            return wrapper
        return decorator

    @staticmethod
    def program_time():
        return perf_counter() - prog_start

    def __have_stage(self, item):
        return self.all_time.get(item)

    def __add_new_stage(self, item):
        self.all_time[item] = [self.last_interval]

    def __getitem__(self, item):
        return self.all_time[item] if item not in ("last", -1) else self.last_interval

    def __iter__(self):
        return iter({key: sum(el) for key, el in self.all_time.items()}.items())

    def __str__(self):
        return str(self.all_time)
